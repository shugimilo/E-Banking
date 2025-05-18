from gui.app import App
from gui.signin import SignIn

def main():
    app = App()
    app.switch_frame(SignIn)
    app.mainloop()

if __name__ == "__main__":
    main()