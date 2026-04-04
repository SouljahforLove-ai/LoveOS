class IdentityState:
    SIGIL = "N2 m(THYSELF)e | 👁️ ."

    def load(self):
        return {
            "sigil": self.SIGIL,
            "status": "identity_loaded"
        }
