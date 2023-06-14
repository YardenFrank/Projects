import java.util.*;
public class Finding_Primes_Java
{
    public static Scanner reader = new Scanner(System.in);
    
    public static void main(String[] args)
    {
        int num = (-1);
        while(num<1) {
            System.out.println("Enter a number:");
            num = reader.nextInt();
        }
        System.out.println("factors: "+numInPrime(num));
    }
    
    //returns if number is prime
    public static boolean isPrime(int num)
    {
        for(int i = 2; i <= (Math.sqrt(num)); i++)
        {
            if(num % i == 0)
                return false;
        }
        return(num!=1);
    }
    
    // returns the next prime number after num
    public static int nextPrime(int num)
    {
        num++;
        if(num%2==0)
            num++;
        while(!isPrime(num))
            num+=2;
        return num;
    }
    
    // returns a String containing all of the number's prime factors.
    public static String numInPrime(int num)
    {
        if(num==1)
            return "1 has no prime factors.";
        String numinprime = "";
        int checker = 2, limitnum = (int)Math.sqrt(num), counter = 0;
        
        for(; checker <= limitnum; checker = nextPrime(checker))
        {
            while(num % checker==0) {
                counter++;
                num /= checker;
            }
            if(counter>1)
                numinprime+=checker+"^"+counter+" ";
            else {
                if (counter > 0)
                    numinprime+=checker+" ";
            }
            counter = 0;
        }
        
        if(num!=1)
            numinprime+=num;
        return numinprime;
    }
}

