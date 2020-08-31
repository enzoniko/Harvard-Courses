using UnityEngine;
public class TimerBar : MonoBehaviour
{
    public GameObject bar;
    void Update()
    {
        if ( Database.timeLeft > 0)
        {
            Database.timeLeft -= Time.deltaTime;
            float barX = Database.timeLeft / Database.maxTime;
            //Debug.Log(Database.maxTime);
            Vector3 barScale = new Vector3(barX, 1, 1);
            bar.GetComponent<RectTransform>().localScale = barScale;
        } else {
            DataBaseManager.goToScene("GameOver");
            FindObjectOfType<AudioManager>().Play("GameOver");
        }
    }
}
