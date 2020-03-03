/*
Package notes is going to be an awesome. This module is coming soon. Please
await further changes on this.

		Long description for root notes

		Usage:
			notes [flags]
			notes [command]

		Available Commands:
			help        Help about any command
			new         A brief description of your command
			pull        A brief description of your command
			push        A brief description of your command
			save        A brief description of your command

		Flags:
					--config string   config file (default is $HOME/.notes.yaml)
			-h, --help            help for notes
			-t, --toggle          Help message for toggle

		Use "notes [command] --help" for more information about a command.

License

Copyright © 2020 Harman <hrmnjt@hrmn.in>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
package main

import "github.com/hrmnjt/notes/cmd"

func main() {
	cmd.Execute()
}
