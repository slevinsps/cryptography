#include <stdio.h>
#include <iostream>
#include <stdio.h>
#include <string>
#include <fstream>

#include "run_bash_command.h"


int check_istallation() {
  std::string currentCode = execBash("echo $(sudo dmidecode -t 4 | grep ID | sed 's/.*ID://;s/ //g') | sha256sum | awk '{print $1}'");
  currentCode.erase(currentCode.length()-1);

  std::string codeFromFile = "";
  int err = 0;
  std::ifstream in("code.calc"); 
  if (in.is_open())
  {
    getline(in, codeFromFile);
  } else {
    err = -1;
  }
  in.close();
  // std::cout << codeFromFile << "#\n" << currentCode << "#";
  if (err == 0 && codeFromFile != currentCode) {
    err = -2;
  }
  return err;
}

double sum(double a, double b){
  return a + b;
} 

double mul(double a, double b){
  return a * b;
} 

double div(double a, double b){
  if (b == 0) {
    return 0;
  }
  return a / b;
} 

double sub(double a, double b){
  return a - b;
} 

int calculate(double a, char op, double b, double *ans){
  int err = 0;
  switch (op) {
    case '+':
      *ans = sum(a, b);
      break;
    case '*':
      *ans = mul(a, b);
      break;
    case '/':
      if (b == 0) {
        err = -2;
      } else {
        *ans = div(a, b);
      }
      break;
    case '-':
      *ans = sub(a, b);
      break;
    default:
      *ans = -1;
      err = -1;
      break;
  }
  return err;
}

int main(){

  int errInstall = check_istallation();
  switch (errInstall) {
    case -1:
      printf("File code.calc not found, program couldn`t run on this computer\n");
      return -1;
    case -2:
      printf("Program not installed on this computer\n");
      return -2;
  }

  double a, b;
  char op;
  printf("Enter a, operations(+, -, /, *) and b space-separated:\n");
  int out = -1; 

  out = scanf("%lf %c %lf", &a, &op, &b);
  if (out != 3) {
    printf("Invalid input\n");
    return 0;
  }

  double ans = 0;
  int err = calculate(a, op, b, &ans);

  if (err == -1) {
    printf("Invalid operation");
  } else if (err == -2) {
    printf("Division by zero");
  } else {
    printf("%lf  %c  %lf = %lf", a, op, b, ans);
  }

  return 0;
}