// FUNCTIONS

// Functions allow you to easily re-use and call code segments!

////////////////////
// GENERAL FORMAT //
////////////////////

// def functionName(input1:type,intput2:type): return type = {
//    do stuff
//                     }

// Examples

def simple(): Unit = {
  println("Simple Print")
}
simple()

// Adding two inputs
def adder(num1:Int,num2:Int): Int = {
  return num1 + num2
}

val x = adder(2,3)
println(x)

// Greeting Someone
def greetName(name:String): String = {
  return s"Hello $name"
}
val fullgreet = greetName("Jose")
println(fullgreet)

// Check if a number is prime
def isPrime(numcheck:Int): Boolean = {
  for(n <- Range(2,numcheck)){
    if(numcheck%n == 0){
      return false
    }
    }
    return true
}


println(isPrime(10))
println(isPrime(23))

// Using Collections

val numbers = List(1,2,3,7)
def check(nums:List[Int]): List[Int]={
  return nums
}

println(check(numbers))

// "One Line Functions"
def quickgreet(name:String) = s"Hello $name"
println(quickgreet("Sammy"))


def checkEven(num:Int): Boolean{
    if(num%2 == 0){
        return true
    }
    return false
}

// 1.) Check for Single Even:
// Write a function that takes in an integer and returns a Boolean indicating whether
// or not it is even. See if you can write this in one line!

def checkEven(num: Int): Boolean = {
    return num % 2 == 0
}

// 2.) Check for Evens in a List:
// Write a function that returns True if there is an even number inside of a List,
// otherwise, return False.

def checkEvenInList(num_list: List[Int]): Boolean = {
  for(num <- num_list){
    if(checkEven(num) == true){
      return true
    }
  }
  return false
}

// 3.) Lucky Number Seven:
// Take in a list of integers and calculate their sum. However, sevens are lucky
// and they should be counted twice, meaning their value is 14 for the sum. Assume
// the list isn't empty.

def weirdSum(num_list: List[Int]): Int = {
  var sum = 0
  for(num <- num_list){
    if(num == 7){
      sum = sum + 2 * num
    }else{
      sum = sum + num
    }
  }
  return sum
}

// 4.) Can you Balance?
// Given a non-empty list of integers, return true if there is a place to
// split the list so that the sum of the numbers on one side
// is equal to the sum of the numbers on the other side. For example, given the
// list (1,5,3,3) would return true, you can split it in the middle. Another
// example (7,3,4) would return true 3+4=7. Remember you just need to return the
// boolean, not the split index point.

def splittable(num_list: List[Int]): Boolean = {
  var half_sum = num_list.sum / 2.0
  var running_sum = 0
  for(num <- num_list){
    running_sum = running_sum + num
    if(running_sum == half_sum){
      return true
    }
  } return false
}

// 5.) Palindrome Check
// Given a String, return a boolean indicating whether or not it is a palindrome.
// (Spelled the same forwards and backwards). Try exploring methods to help you.

def checkPalindrome(str: String): Boolean = {
  return str == str.reverse
}