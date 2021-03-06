import logging

from PyInquirer import prompt, Separator

main_menu = [
    {
        'type': 'expand',
        'message': 'Debug main menu: ',
        'name': 'main',
        'default': 's',
        'choices': [
            {
                'key': 's',
                'name': 'Step',
                'value': 'cpu_step'
            },
            {
                'key': 'r',
                'name': 'Run',
                'value': 'run'
            },
            {
                'key': 'f',
                'name': 'Fast run to address',
                'value': 'fast-run-to'
            },
            {
                'key': 'a',
                'name': 'Run until address',
                'value': 'run-to'
            },
            {
                'key': 'd',
                'name': 'Dump CPU',
                'value': 'cpu dump'
            },
            {
                'key': 'm',
                'name': 'Dump memory',
                'value': 'memory dump'
            },
            Separator(),
            {
                'key': 'q',
                'name': 'Quit',
                'value': 'quit'
            },
        ]
    }
]

run_to_input = [
    {
        'type': 'input',
        'name': 'address',
        'message': 'Run up to address (hex)',
    }
]

address_to_dump = [
    {
        'type': 'input',
        'name': 'address',
        'message': 'Run up to address (hex)',
    }
]


class DMGDebugger:
    def __init__(self, emulator):
        self.emulator = emulator

    def run(self):
        while True:
            response = prompt(main_menu)
            if response['main'] == 'cpu_step':
                self.emulator.cpu_step()

            elif response['main'] == 'cpu dump':
                print(self.emulator.cpu.dump())

            elif response['main'] == 'memory dump':
                print(self.emulator.memory)

            elif response['main'] == 'run-to':
                response = prompt(run_to_input)
                if response['address'] != '':
                    run_to = int(response['address'], 16)
                    while self.emulator.cpu.register_program_counter.get() != run_to:
                        self.emulator.cpu_step()

            elif response['main'] == 'fast-run-to':
                response = prompt(run_to_input)
                if response['address'] != '':
                    run_to = int(response['address'], 16)
                    logging.getLogger().setLevel(logging.INFO)
                    while self.emulator.cpu.register_program_counter.get() != run_to:
                        self.emulator.cpu_step()
                    logging.getLogger().setLevel(logging.DEBUG)

            elif response['main'] == 'quit':
                break

            elif response['main'] == 'run':
                self.emulator.run()
