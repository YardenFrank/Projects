import java.util.Scanner;
//אנימציה של עיגול הולך וקטן

public class CircleAnimation
{
    public static Scanner reader = new Scanner(System.in);
	public static void main(String[] args)
	{
	    
		
		int rad; //רדיוס המעגל
		int counter; //הפריים הנוכחי
		
		boolean again = true;
		
		char kelet; //המשתמש מכניס אם להמשיך או לא
		
		
		while(again)
	    {
	        counter = 1;
	        System.out.println("Enter starting radius:");
		    rad = reader.nextInt();
	        
	        
    		for(int x = 0; x < rad; x++) // לולאה חיצונית - כמות הפעמים שתצוייר האנימציה
    		{
                //ציור העיגול
                draw(rad, counter);
        		
        		counter++;
        		
        		//הזמן במילישניות שיעבור בין כל פריים
        		wait(50);
    	    }
    	    
    	    
    	    wait(500);
    	    //לולאה לפי רצון המשתמש
    	    System.out.println("again?");
    	    kelet = reader.next().charAt(0);
    	    if(kelet != 'y' && kelet != 'ט')
    	        again = false;
	    }
	}
	
	
	
	
	//הפעולה מציירת את העיגול הנוכחי
	public static void draw(int rad, int counter)
	{
	    int distance;
	    
	    
	    //לולאת שורות
		for(int i = 0; i <= rad*2-counter; i++)
		{
		    
    	    //לולאת טורים
    	    for(int j = 0 ; j <= rad*2-counter; j++)
            {
                
        	    //מציאת האם הנקודה נמצאת בעיגול
        	    distance = (int)(Math.sqrt((i-rad)*(i-rad)*4+(j-rad)*(j-rad))); //הסבר למטה
            		        
                if(distance > rad-counter)
                    System.out.print(" ");
                else
                    System.out.print(".");
            }
            
            
            System.out.println();
		}
	}
	
	
	
	
	//פעולת זמן - העתקתי מהאינטרנט
	public static void wait(int ms)
    {
        try
        {
            Thread.sleep(ms);
        }
        
        catch(InterruptedException ex)
        {
            Thread.currentThread().interrupt();
        }
    }
    
    /*
    את הנוסחה למרחק מביעים באמצעות נוסחת דיסטנס ומכפילים את ערך השורות פי 4  מכיוון שבאדיטור אם לא מכפילים הציור יוצא עקום.
    */
}
