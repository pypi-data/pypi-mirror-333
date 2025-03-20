import sys
from NeutroSpecUI import NeutroApp

if __name__ == "__main__":
    app = NeutroApp(sys.argv)

    sys.exit(app.start_neutro())
