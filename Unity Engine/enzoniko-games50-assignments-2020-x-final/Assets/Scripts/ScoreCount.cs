using UnityEngine;
using UnityEngine.UI;

public class ScoreCount : MonoBehaviour
{
    public Text scoreText;
    
    void Update()
    {
        if (scoreText)
        {
            scoreText.text = "SCORE: " + Database.score;
        }  
    }
}
