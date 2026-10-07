public class hello {
    public static void main(string[] args) {
        string name = "Alex";
        int age = 21;

        system.out.println("Name: " + name);
        system.out.println("Age: " + age);

        if (age >=18) {
            system.out.println("Adult");
        }
        else {
            system.out.println("Minor");
        }
    }
}

public class calc {
    public static void main(string[] args) {
        int a = 10;
        int b = 3;

        sum = a + b;
        product = a*b;
        quot= a/b;
        diff= a - b;

        system.out.println("Sum: " + sum);
        system.out.println("Product: " + product);
        system.out.println("Quotiate: " + quot);
        system.out.println("Difference: " + diff);
    }
}

public class Grades {
    public static void main(String[] args) {
        int score = 85;

        if (score >= 70) {
            System.out.println(String.format("Score: %d,  Grade: A", score));
        } else if (score >= 60) {
            System.out.println(String.format("Score: %d , Grade: B", score));
        } else if (score >= 50) {
            System.out.println(String.format("Score: %d , Grade: C", score));
        } else {
            System.out.println(String.format("Score: %d , Grade: f", score));
        }
    }
}


public class Math123 {
    public static int add(int a, int b) {
        return a + b;
    }
    public static int multiply(int a, int b) {
        return a*b;
    }
    public static double average(int a, int b) {
        return add(a,b)/2.0;
    }

    public static void main(String[] args) {
        int a = 10;
        int b = 4;

        int res1 = add(a,b);
        int res2 = average(a,b);
        double res3 = multiply(a,b);

        System.out.println(String.format("Addition: %d ", res1));
        System.out.println(String.format("Average: %f", res2));
        System.out.println(String.format("Multiply: %d", res3));
    }
}


public class Calc2 {
    public double average(int a, int b) {
        return add(a,b)/2.0;
    }
    public int add(int a, int b) {
        return a + b;
    }
    public double div(int a, int b) {
        return (double) a/b;
    }
    public int diff(int a, int b) {
        return a - b;
    }
    public int multiply(int a, int b) {
        return a*b;
    }

    public static void main(String[] args){
        Calc2 m = new Calc2();
        int resp1 = m.add(10,20);
        double resp2 = m.average(10,20);
        double resp3 = m.div(20,10);
        int resp4 = m.diff(20,10);
        int resp5 = m.multiply(20,10);

         System.out.println("Addition: " + resp1);
         System.out.println("Average: " + resp2);
         System.out.println("Division: " + resp3);
         System.out.println("Difference: " + resp4);
         System.out.println("Multiply: " + resp5);
       
    }



    
}