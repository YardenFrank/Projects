package Bagrut;
import Matconet.AProject1;
import unit4.collectionsLib.Node;
import unit4.collectionsLib.BinNode;
import unit4.binTreeUtilsLib.BinTreeUtils;
import unit4.binTreeCanvasLib.BinTreeCanvas;
import unit4.collectionsLib.Queue;

public class AprojectBagrut1
{
    public static void main(String[] args)
    {
        int[] arr = {-3, -3,5, 9, -3, 17, 29, -20, -40, 28};
        System.out.println(posOrder(arr));
    }


    public static boolean numInTree(BinNode<Integer> tree, int num)
    {
        if(tree.getValue() == num)
            return true;

        if(tree.hasLeft())
            if(numInTree(tree.getLeft(), num))
                return true;

        if(tree.hasRight())
            if(numInTree(tree.getRight(), num))
                return true;

        return false;
    }

    public static Queue<Integer> reverse(Queue<Integer> q)
    {
        int num;
        if(! q.isEmpty())
        {
            num = q.remove();
            q = reverse(q);
            q.insert(num);
        }

        return q;
    }

    public static int missingNum(int[] arr)
    {
        int index = 1;
        int minus = arr[1] - arr[0];
        boolean check = true;

        while(index < arr.length && check)
        {
            if(arr[index] - arr[index - 1] != minus)
                check = false;
            else
                index++;
        }

        if(arr[index] - arr[index - 1] == 2 * minus)
            return arr[index] - minus;
        return arr[0] + minus / 2;
    }

    public static boolean twoSum(Queue<Integer> q, int x)
    {
        int i = 1;
        int size = size(q);
        int num = q.remove();

        while(i < size)
        {
            for(int j = 0; j < size - 1; j++)
            {
                if(q.head() == x - num)
                    return true;
            }

            q.insert(num);
            num = q.remove();
            i++;
        }
        return false;
    }

    public static int size(Queue<Integer> q)
    {
        int count = 0;
        q.insert(null);
        while(q.head() != null)
        {
            q.insert(q.remove());
            count++;
        }
        q.remove();
        return count;
    }

    public static boolean posOrder(int[] arr)
    {
        int num = 0;
        int i = 0;
        boolean check = true;

        while(i < arr.length && check)
        {
            if(arr[i] > 0)
            {
                num = arr[i];
                check = false;
            }
            i++;
        }
        check = true;

        for(int j = i + 1; j < arr.length; j++)
        {
            if(arr[j] > 0) {
                if (arr[j] < num)
                    check = false;
                else
                    num = arr[j];
            }
        }

        return check;
    }



}
