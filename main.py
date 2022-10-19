from src.mediators.main_mediator import MainMediator


def main():
    MainMediator() \
        .apply_local_config() \
        .apply_arguments_config() \
        .load_inputs() \
        .run_pipeline() \
        .closure()

if __name__ == '__main__':
    main()
