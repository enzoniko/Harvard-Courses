using UnityEngine;
using UnityEngine.SceneManagement;

public class DataBaseManager : MonoBehaviour
{
    public static void refreshCurrentScene()
    {
        Database.currentScene = SceneManager.GetActiveScene().name;
    }
    public static void getFoodValueForGameMode()
    {
        if (Database.currentScene == "1PlayerMode")
        {
            Database.foodValue = 0.1f;
        } else {
            Database.foodValue = 1f;
        }
    }
    public static void reduceFoodValueBy(float amount)
    {
        Database.foodValue -= amount;
    }
    public static void setFoodValueTo(float amount)
    {
        Database.foodValue = amount;
    }

    public static void increaseBlackHoleCubesNumber()
    {
        Database.blackHoleCubesNumber ++;
    }
    public static void handleRoundChanging()
    {
        if (Database.foodValue <= 0)
        {
            Database.maxTime = 30f;
            Database.foodValue = 1f;
            goToScene("GameOver");
        } else {
            goToScene("QuickMode");
            newRound();
        }
    }
    public static void goToScene(string scene)
    {
        SceneManager.LoadScene(scene);
    }
    public static void addScore(int amount)
    {
        Database.score += amount;
    }
    public static void resetScore()
    {
        Database.score = 0;
    }
    public static void newRound()
    {
        Database.round ++;
    }
    public static void resetRound()
    {
        Database.round = 1;
    }
    public static void resetHealths()
    {
        Database.maxHealth = 3;
        Database.currentHealth = Database.maxHealth;
    }
    public static void resetTimes()
    {
        Database.maxTime = 30f;
        Database.timeLeft = Database.maxTime;
    }
    public static void AddSeconds(float seconds)
    {
        Database.timeLeft = Mathf.Clamp(Database.timeLeft + seconds, 0, Database.maxTime);
    }

    public static void resetAllAndGoToScene(string scene)
    {
        resetTimes();
        resetHealths();
        goToScene(scene);
        resetRound();
        resetScore();
        getFoodValueForGameMode();
        
    }
}
