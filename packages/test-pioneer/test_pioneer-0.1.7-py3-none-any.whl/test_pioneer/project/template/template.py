template_1_str: str = \
"""
pioneer_log: "test_pioneer.log"
jobs:
    steps:
        - name: run_test_script_1
          run: test/test1.json
          with: gui-runner
        - name: wait_seconds
          wait: 5
        - name: run_test_script_1
          run: test/test1.json
          with: gui-runner
"""
