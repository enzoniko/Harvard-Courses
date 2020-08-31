using UnityEngine;
public class goBack : MonoBehaviour
{
    // Update is called once per frame
    void LateUpdate()
    {
        //if (Input.GetKeyDown(KeyCode.Return))
        //{
            //DataBaseManager.resetAllAndGoToScene("1PlayerMode");
        //}
        if (Input.GetKeyDown(KeyCode.Return))
        {
            DataBaseManager.resetAllAndGoToScene("QuickMode");
            FindObjectOfType<AudioManager>().Play("StartSound");
            
        }
    }
}
