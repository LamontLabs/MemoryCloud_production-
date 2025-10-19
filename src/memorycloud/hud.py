def render_hud(success: bool, fallback: bool = False) -> str:
    """
    Render simple HUD indicator for demo.
    ✔ = verified signed capture
    ! = fallback (no hardware TEE)
    ✖ = rejected/invalid
    """
    if not success:
        return "✖"
    return "!" if fallback else "✔"
