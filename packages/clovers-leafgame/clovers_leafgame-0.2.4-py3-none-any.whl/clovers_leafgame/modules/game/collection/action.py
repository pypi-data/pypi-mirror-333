import asyncio
from clovers_leafgame.main import plugin, manager
from clovers_leafgame.core.clovers import Event
from ..core import Session, Game

place: dict[str, Session] = {}


@plugin.handle(["接受挑战"], ["user_id", "group_id", "nickname"])
async def _(event: Event):
    group_id = event.group_id
    session = Game.session_check(place, group_id)
    if not session:
        return
    user_id = event.user_id
    if session.p2_uid or session.p1_uid == user_id:
        return
    if session.at and session.at != user_id:
        return f"现在是 {session.p1_nickname} 发起的对决，请等待比赛结束后再开始下一轮..."
    user, account = manager.account(event)
    user.connect = group_id
    bet = session.bet
    if bet:
        prop, n = bet
        if account.bank[prop.id] < n:
            return f"你的无法接受这场对决！\n——你还有{account.bank[prop.id]}个{prop.name}。"
        tip = f"对战金额为 {n} {prop.name}\n"
    else:
        tip = ""
    session.join(user_id, account.name)
    session.next = session.p1_uid
    msg = f"{session.p2_nickname}接受了对决！\n本场对决为【{session.game.name}】\n{tip}请{session.p1_nickname}发送指令\n{session.game.action_tip}"
    if session.start_tips:

        async def result():
            yield msg
            await asyncio.sleep(1)
            yield session.start_tips

        return result()
    return msg


@plugin.handle(["拒绝挑战"], ["user_id", "group_id"])
async def _(event: Event):
    session = Game.session_check(place, event.group_id)
    if session and (at := session.at) and at == event.user_id:
        if session.p2_uid:
            return "对决已开始，拒绝失败。"
        return "拒绝成功，对决已结束。"


@plugin.handle(["超时结算"], ["user_id", "group_id"])
async def _(event: Event):
    if (session := place.get(event.group_id)) and session.timeout() < 0:
        session.win = session.p2_uid if session.next == session.p1_uid else session.p1_uid
        return session.end()


@plugin.handle(["认输"], ["user_id", "group_id"])
async def _(event: Event):
    user_id = event.user_id
    session = place.get(event.group_id)
    if not session or session.p2_uid is None:
        return
    if user_id == session.p1_uid:
        session.win = session.p2_uid
    elif user_id == session.p2_uid:
        session.win = session.p1_uid
    else:
        return
    return session.end()


@plugin.handle(["游戏重置", "清除对战"], ["user_id", "group_id", "permission"])
async def _(event: Event):
    group_id = event.group_id
    session = place.get(group_id)
    if not session:
        return
    if session.timeout() > 0 and event.permission < 1:
        return f"当前游戏未超时。"
    del place[group_id]
    return "游戏已重置。"
