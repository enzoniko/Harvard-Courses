using UnityEngine;
using UnityEngine.UI;

public class RoundCount : MonoBehaviour
{
    public Text roundText;
    
    void Update()
    {
        roundText.text = "ROUND: " + Database.round;
    }
}
