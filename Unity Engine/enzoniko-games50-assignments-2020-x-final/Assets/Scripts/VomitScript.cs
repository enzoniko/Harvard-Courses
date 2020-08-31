using UnityEngine;
public class VomitScript : MonoBehaviour
{
    void Start()
    {
        gameObject.GetComponent<MeshRenderer>().material.color = Database.currentMaterial.color;
        gameObject.GetComponent<MeshRenderer>().material.EnableKeyword("_EMISSION");
        gameObject.GetComponent<MeshRenderer>().material.SetColor("_EmissionColor", Database.currentMaterial.color);
        gameObject.GetComponentInChildren<Light>().color = Database.currentMaterial.color;
 
    }
}
