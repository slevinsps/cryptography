#include <stdlib.h>
#include <stdio.h>
#include <string>
#include <fstream>

#include "run_bash_command.h"

int main() {
  std::ofstream outfile ("code.calc");
  std::string result = execBash("echo $(sudo dmidecode -t 4 | grep ID | sed 's/.*ID://;s/ //g') | sha256sum | awk '{print $1}'");
  outfile << result;
  outfile.close();
}