"""
run the game, optionally with profiling ...
"""

def _run_app():
    from gravbot.app import App
    app = App()
    app.run()


def _run__test_app():
    from gravbot.mc import App
    app = App()
    app.run()

def _complain_about_usage_and_die():
    sys.stderr.write('usage: [--profile]')
    sys.exit(1)

def main():
    import sys
    options = {
        '--profile': False,
	'--test':False,
    }


    for arg in sys.argv[1:]:
        if arg not in options:
            _complain_about_usage_and_die()
        else:
            options[arg] = True

    if options['--profile']:
        import pstats
        import cProfile
        p = cProfile.Profile()
        def _wrapper():
            try:
                _run_app()
            except SystemExit, KeyboardInterrupt:
                pass
        p.runcall(_wrapper)
        s = pstats.Stats(p)
        s.sort_stats('cumulative').print_stats(25)
    if options['--test']:
        _run_test_app()
    else:
        _run_app()

if __name__ == '__main__':
    main()

