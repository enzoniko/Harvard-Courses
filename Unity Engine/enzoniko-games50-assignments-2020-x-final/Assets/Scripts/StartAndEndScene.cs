using UnityEngine;
using UnityEngine.UI;

public class StartAndEndScene : MonoBehaviour
{
    public Text headerText;

    public Text roundText;

    public Text scoreText;

    public Text explanationText;

    // Update is called once per frame
    void Update()
    {
        if (Database.first == true)
        {
            Database.first = false;
            headerText.text = "FEED HIM";
            roundText.enabled = false;
            scoreText.enabled = false;
            explanationText.text = "By consuming the pink cubes you gain mass,\n feed the black hole with that mass by pressing B close to the black hole,\n be carefull with the time and try not to fall into the void,\n I bet you can't pass round 10. Press ENTER when you are ready.\n Use WASD to move and SPACE to jump.";
            explanationText.gameObject.GetComponent<RectTransform>().localPosition = new Vector3(0, -65f, 0);
        } 
        if (Database.score >= 0 && Database.timeLeft < Database.maxTime && Database.first == false) {
            headerText.text = "GAME OVER";
            roundText.enabled = true;
            scoreText.enabled = true;
            explanationText.text = "Haha, I knew you couldn't do it, press Enter to try again";
            explanationText.gameObject.GetComponent<RectTransform>().localPosition = new Vector3(0, -55f, 0);
        }
        if (Database.round == 10) {
            headerText.text = "YOU FED HIM";
            roundText.enabled = true;
            scoreText.enabled = true;
            explanationText.text = "I can't believe you did it, Congratulations! Press Enter to play again";
            explanationText.gameObject.GetComponent<RectTransform>().localPosition = new Vector3(0, -55f, 0);
        }
    }
}
