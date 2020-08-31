using UnityEngine;
using UnityEngine.UI;
public class HealthBar : MonoBehaviour
{
	public Slider slider;
	public Gradient gradient;
	public Image fill;

	void Start()
	{
		slider.maxValue = Database.maxHealth;
		slider.value = Database.currentHealth;
		fill.color = gradient.Evaluate(1f);
	}

    public void SetHealth(int health)
	{
		slider.value = health;
		fill.color = gradient.Evaluate(slider.normalizedValue);
	}

}
