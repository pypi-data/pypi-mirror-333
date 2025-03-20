from sys import argv


def main():
    if len(argv) >= 2:
        _, subcmd, *_ = argv

        if subcmd.lower() == 'pull':
            print("""gut: Oho that hurts
gut: Maybe you mean "git pull\"""")
        else:
            print("""gut: I don't understand that command.""")
        exit(1)
    else:
        print("""gut: Shortcut to your body part.""")


if __name__ == '__main__':
    main()
