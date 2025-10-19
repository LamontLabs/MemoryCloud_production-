from src.memorycloud.hud import render_hud

def test_hud_render_variants():
    assert render_hud(True) == "✔"
    assert render_hud(True, fallback=True) == "!"
    assert render_hud(False) == "✖"
