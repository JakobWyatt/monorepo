import java.util.*;

public class Input {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        while (!sc.hasNext("[asdf]")) {
            System.out.println("Invalid");
            sc.next();
        }
        sc.next("[asdf]");
    }
}
