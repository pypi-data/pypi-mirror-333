from aw.config.main import config

FORM_LABEL = {
    'jobs': {
        'manage': {
            'repository': 'Repository',
            'environment_vars': 'Environmental Variables',
            'mode_diff': 'Diff Mode',
            'mode_check': 'Check Mode (Try Run)',
            'cmd_args': 'Commandline Arguments',
            'enabled': 'Schedule Enabled',
            'tags_skip': 'Skip Tags',
            'credentials_needed': 'Needs Credentials',
            'credentials_default': 'Default Job Credentials',
            'credentials_category': 'Credentials Category',
            'execution_prompts_required': 'Execution Prompts - Required',
            'execution_prompts_optional': 'Execution Prompts - Optional',
        },
        'credentials': {
            'connect_user': 'Connect User',
            'connect_pass': 'Connect Password',
            'become_user': 'Become User',
            'become_pass': 'Become Password',
            'vault_file': 'Vault Password File',
            'vault_pass': 'Vault Password',
            'vault_id': 'Vault ID',
            'ssh_key': 'SSH Private Key',
            'category': 'Category',
        },
        'repository': {
            'rtype': 'Repository Type',
            'static_path': 'Static Repository Path',
            'git_origin': 'Git Origin',
            'git_branch': 'Git Branch',
            'git_credentials': 'Git Credentials',
            'git_limit_depth': 'Git Limit Depth',
            'git_lfs': 'Git LFS',
            'git_playbook_base': 'Git Playbook Base-Directory',
            'git_isolate': 'Git Isolate Directory',
            'git_hook_pre': 'Git Pre-Hook',
            'git_hook_post': 'Git Post-Hook',
            'git_hook_cleanup': 'Git Cleanup-Hook',
            'git_override_initialize': 'Git Override Initialize-Command',
            'git_override_update': 'Git Override Update-Command',
        },
    },
    'settings': {
        'permissions': {
            'jobs_all': 'All jobs',
            'credentials_all': 'All credentials',
            'repositories_all': 'All repositories',
        },
        'alerts': {
            'alert_type': 'Alert Type',
            'plugin': 'Plugin',
            'jobs_all': 'All Jobs',
            'jobs': 'Jobs',
            'condition': 'Condition',
        }
    },
    'system': {
        'config': {
            'path_run': 'Runtime directory',
            'path_play': 'Playbook base-directory',
            'path_log': 'Directory for execution-logs',
            'path_template': 'Directory for templates',
            'run_timeout': 'Timeout for playbook execution',
            'session_timeout': 'Timeout for WebUI login-sessions',
            'path_ansible_config': 'Ansible Config-File',
            'path_ssh_known_hosts': 'SSH Known-Hosts File',
            'debug': 'Debug Mode',
            # env-vars
            'timezone': 'Timezone',
            'db': 'Database',
            'hostnames': 'Hostnames',
            'proxy': 'Using Proxy',
            'db_migrate': 'Database auto-upgrade',
            'serve_static': 'Serving static files',
            'deployment': 'Deployment',
            'version': 'Ansible-WebUI Version',
            'logo_url': 'URL to a Logo to use',
            'ara_server': 'ARA Server URL',
            'global_environment_vars': 'Global Environmental Variables',
            'auth_mode': 'Authentication Mode',
            'saml_config': 'SAML Config File',
            'address': 'Listen Address',
            'port': 'Listen Port',
            'ssl_file_crt': 'SSL Certificate',
            'ssl_file_key': 'SSL Private-Key',
            'mail_server': 'Mail Server',
            'mail_transport': 'Mail Transport',
            'mail_ssl_verify': 'Mail SSL Verification',
            'mail_sender': 'Mail Sender Address',
            'mail_user': 'Mail Login Username',
            'mail_pass': 'Mail Login Password',
        }
    }
}

FORM_HELP = {
    'jobs': {
        'manage': {
            'playbook_file': f"Playbook to execute. Search path: '{config['path_play']}'",
            # todo: change search-path with repository
            'inventory_file': 'One or multiple inventory files/directories to include for the execution. '
                              'Comma-separated list. For details see: '
                              '<a href="https://docs.ansible.com/ansible/latest/inventory_guide/'
                              'intro_inventory.html">Ansible Docs - Inventory</a>',
            'repository': 'Used to define the static or dynamic source of your playbook directory structure. '
                          f"Default is '{config['path_play']}'",
            'limit': 'Ansible inventory hosts or groups to limit the execution to.'
                     'For details see: '
                     '<a href="https://docs.ansible.com/ansible/latest/inventory_guide/intro_patterns.html">'
                     'Ansible Docs - Limit</a>',
            'schedule': 'Schedule for running the job automatically. For format see: '
                        '<a href="https://crontab.guru/">crontab.guru</a>',
            'environment_vars': 'Environmental variables to be passed to the Ansible execution. '
                                'Comma-separated list of key-value pairs. (VAR1=TEST1,VAR2=0)',
            'cmd_args': "Additional commandline arguments to pass to 'ansible-playbook'. "
                        "Can be used to pass extra-vars",
            'tags': 'For details see: '
                    '<a href="https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_tags.html">'
                    'Ansible Docs - Tags</a>',
            'mode_check': 'For details see: '
                          '<a href="https://docs.ansible.com/ansible/2.8/user_guide/playbooks_checkmode.html">'
                          'Ansible Docs - Check Mode</a>',
            'credentials_needed': 'If the job requires credentials to be specified '
                                  '(either as default or at execution-time; '
                                  'fallback are the user-credentials of the executing user)',
            'credentials_default': 'Specify job-level default credentials to use',
            'credentials_category': 'The credential category can be used for dynamic matching of '
                                    'user credentials at execution time',
            'enabled': 'En- or disable the schedule. Can be ignored if no schedule was set',
            'execution_prompts_required': 'Required job attributes and/or variables to prompt at custom execution. '
                                          'Comma-separated list of key-value pairs.<br>'
                                          "Variables can be supplied like so: 'var={VAR-NAME}#{DISPLAY-NAME}'<br>"
                                          "Example: 'limit,check,var=add_user#User to add' ",
        },
        'credentials': {
            'vault_file': 'Path to the file containing your vault-password',
            'vault_id': 'For details see: '
                        '<a href="https://docs.ansible.com/ansible/latest/vault_guide/'
                        'vault_managing_passwords.html">'
                        'Ansible Docs - Managing Passwords</a>',
            'ssh_key': 'Provide an unencrypted SSH private key',
            'category': 'The category of user credentials. Used for dynamic matching at execution time',
        },
        'repository': {
            'static_path': 'Path to the local static repository/playbook-base-directory',
            'git_origin': "Full URL to the remote repository. "
                          "Per example: '<a href=\"https://github.com/O-X-L/ansible-webui.git\">"
                          "https://github.com/O-X-L/ansible-webui.git'</a>'",
            'git_credentials': "Credentials for connecting to the origin. "
                               "'Connect User', 'Connect Password' and 'SSH Private Key' are used",
            'git_playbook_base': 'Relative path to the Playbook base-directory relative from the repository root',
            'git_lfs': 'En- or disable checkout of Git-LFS files',
            'git_isolate': 'En- or disable if one clone of the Git-repository should be used for all jobs. '
                           'If enabled - the repository will be cloned/fetched on every job execution. '
                           'This will have a negative impact on performance',
            'git_hook_pre': 'Commands to execute before initializing/updating the repository. '
                            'Comma-separated list of shell-commands',
            'git_hook_post': 'Commands to execute after initializing/updating the repository. '
                             'Comma-separated list of shell-commands',
            'git_override_initialize': 'Advanced usage! Completely override the command used to initialize '
                                       '(clone) the repository',
            'git_override_update': 'Advanced usage! Completely override the command used to update '
                                   '(pull) the repository',
        },
    },
    'settings': {
        'permissions': {
            'jobs_all': 'Match permission to all existing jobs (present and future)',
            'credentials_all': 'Match permission to all existing credentials (present and future)',
            'repositories_all': 'Match permission to all existing repositories (present and future)',
        },
        'alerts': {
            'jobs_all': 'Match all existing jobs (present and future)',
        }
    },
    'system': {
        'config': {
            'path_run': 'Base directory for <a href="https://ansible.readthedocs.io/projects/runner/en/latest/intro/">'
                        'Ansible-Runner runtime files</a>',
            'path_play': 'Path to the <a href="https://docs.ansible.com/ansible/2.8/user_guide/'
                         'playbooks_best_practices.html#directory-layout">Ansible base/playbook directory</a>',
            'path_log': 'Define the path where full job-logs are saved',
            'path_template': 'Define the path where custom templates are placed',
            'path_ansible_config': 'Path to a <a href="https://docs.ansible.com/ansible/latest/installation_guide'
                                   '/intro_configuration.html#configuration-file">Ansible config-file</a> to use',
            'path_ssh_known_hosts': 'Path to a <a href="https://en.wikibooks.org/wiki/OpenSSH/'
                                    'Client_Configuration_Files#~/.ssh/known_hosts">SSH known_hosts file</a> to use',
            'debug': 'Enable Debug-mode. Do not enable permanent on production systems! '
                     'It can possibly open attack vectors. '
                     'You might need to restart the application to apply this setting',
            'logo_url': 'Default: <a href="/static/img/logo.svg">img/logo.svg</a>; '
                        'Per example: '
                        '<a href="https://raw.githubusercontent.com/ansible/logos/main/vscode-ansible-logo'
                        '/vscode-ansible.svg">'
                        'https://raw.githubusercontent.com/ansible/logos/main/vscode-ansible-logo/vscode-ansible.svg'
                        '</a>',
            'ara_server': 'Provide the URL to your ARA server. Can be used to gather job statistics. See: '
                          '<a href="https://webui.ansibleguy.net/usage/integrations.html">'
                          'Documentation - Integrations</a>',
            'global_environment_vars': 'Set environmental variables that will be added to every job execution. '
                                       'Comma-separated list of key-value pairs. (VAR1=TEST1,VAR2=0)',
            'mail_server': 'Mail Server to use for Alert Mails. Combination of server and port (default 25)',
            'mail_ssl_verify': 'En- or disable SSL certificate verification. '
                               'If enabled - the certificate SAN has to contain the mail-server FQDN '
                               'and must be issued from a trusted CA',
            'mail_sender': 'Mail Sender Address to use for Alert Mails. Fallback is mail-user',
            'mail_transport': 'The default port mapping is: 25 = Unencrypted, 465 = SSL, 587 = StartTLS',
        }
    }
}
