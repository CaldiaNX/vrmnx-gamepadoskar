__title__ = "ゲームパッド押すかーくん Ver.1.0"
__author__ = "Caldia"
__update__  = "2025/03/09"

"""
レイアウトスクリプトに以下の★内容を追記してください。
import vrmapi
import gamepadoskar # ★スクリプトインポート

def vrmevent(obj,ev,param):
    gamepadoskar.vrmevent(obj,ev,param) # ★メイン処理
"""

import vrmapi

# ファイル読み込みの確認用
vrmapi.LOG("import " + __title__ + " by " + __author__)
# ウィンドウ描画フラグ
_drawEnable = True
# DirectInputのLimit
_IN_MAX = 32767
_IN_MIN = -32768

# main
def vrmevent(obj,ev,param):
    global _drawEnable
    if ev == 'init':
        # フレームイベント登録
        obj.SetEventFrame()
        # pキー登録
        obj.SetEventKeyDown('P')
        # レイアウトDict呼出し
        l_di = obj.GetDict()
        # SetGamepadButtonEnable初期化
        l_di['pad_ena1'] = [0]
        l_di['pad_ena2'] = [0]
        l_di['pad_ena3'] = [0]
        l_di['pad_ena4'] = [0]
    elif ev == 'frame':
        # ウィンドウ描画状態の確認
        if _drawEnable:
            # ウィンドウ描画
            drawFrame(obj)
    elif ev == 'keydown':
        # ウィンドウ描画のON/OFF
        if param['keycode'] == 'P':
            # ウィンドウ描画状態を反転
            _drawEnable = not _drawEnable


# ウィンドウ描画
def drawFrame(obj):

    global __title__
    # ImGui定義
    gui = vrmapi.ImGui()
    gui.Begin("pad_win", __title__)
    # レイアウトDict呼出し
    l_di = obj.GetDict()
    # ゲームパッドごとの状態描画
    drawPadTree(gui, 0, "1", l_di['pad_ena1'])
    drawPadTree(gui, 1, "2", l_di['pad_ena2'])
    drawPadTree(gui, 2, "3", l_di['pad_ena3'])
    drawPadTree(gui, 3, "4", l_di['pad_ena4'])

    gui.End()


# ゲームパッドごとの状態描画
def drawPadTree(gui, iDev, tDev, aryEna):
    vrmsys = vrmapi.SYSTEM()
    # デバイスの接続状態を取得
    b_igc = vrmsys.IsGamepadConnected(iDev)
    t_igc = "未接続"
    if b_igc:
        t_igc = "認識"
    if gui.TreeNode("pad_com" + tDev, "ゲームパッド" + tDev + "：" + t_igc):
        # 認識していれば描画
        if b_igc:
            gui.Checkbox("pad_lt" + tDev, "←", [vrmsys.GetGamepadLEFT(iDev)])
            gui.SameLine()
            gui.Checkbox("pad_up" + tDev, "↑", [vrmsys.GetGamepadUP(iDev)])
            gui.SameLine()
            gui.Checkbox("pad_dn" + tDev, "↓", [vrmsys.GetGamepadDOWN(iDev)])
            gui.SameLine()
            gui.Checkbox("pad_rt" + tDev, "→", [vrmsys.GetGamepadRIGHT(iDev)])

            gui.Checkbox("pad_a" + tDev, "A ", [vrmsys.GetGamepadA(iDev)])
            gui.SameLine()
            gui.Checkbox("pad_b" + tDev, "B ", [vrmsys.GetGamepadB(iDev)])
            gui.SameLine()
            gui.Checkbox("pad_x" + tDev, "X ", [vrmsys.GetGamepadX(iDev)])
            gui.SameLine()
            gui.Checkbox("pad_y" + tDev, "Y ", [vrmsys.GetGamepadY(iDev)])

            gui.Checkbox("pad_lb" + tDev, "L ", [vrmsys.GetGamepadLB(iDev)])
            gui.SameLine()
            gui.Checkbox("pad_rb" + tDev, "R ", [vrmsys.GetGamepadRB(iDev)])
            gui.SameLine()
            gui.Checkbox("pad_st" + tDev, "St", [vrmsys.GetGamepadSTART(iDev)])
            gui.SameLine()
            gui.Checkbox("pad_sl" + tDev, "Bk", [vrmsys.GetGamepadBACK(iDev)])

            global _IN_MAX
            global _IN_MIN

            gui.PushItemWidth(40.0)
            gui.SliderInt("pad_alx" + tDev, "←→", [vrmsys.GetGamepadAnalogStickLX(iDev)], _IN_MIN, _IN_MAX)
            gui.SameLine()
            gui.SliderInt("pad_aly" + tDev, "↑↓ Analog L", [vrmsys.GetGamepadAnalogStickLY(iDev)],_IN_MIN, _IN_MAX)

            gui.SliderInt("pad_arx" + tDev, "←→", [vrmsys.GetGamepadAnalogStickRX(iDev)],_IN_MIN, _IN_MAX)
            gui.SameLine()
            gui.SliderInt("pad_ary" + tDev, "↑↓ Analog R", [vrmsys.GetGamepadAnalogStickRY(iDev)],_IN_MIN, _IN_MAX)
            gui.PopItemWidth()

            if gui.Checkbox("pad_ena" + tDev, "入力制限(競合注意)", aryEna):
                # ボタンをスクリプトで専有するか設定
                setGamepadButtonEnableAll(vrmsys, iDev, aryEna[0])
        gui.TreePop()


# ボタンをスクリプトで専有するか設定
def setGamepadButtonEnableAll(vrmsys, iDev, bEna):
    bt_list = [1, 2, 4, 8, 0x10, 0x20, 0x100, 0x200, 0x1000, 0x2000, 0x4000, 0x8000]
    for k in bt_list:
        vrmsys.SetGamepadButtonEnable(iDev, k, bEna)
