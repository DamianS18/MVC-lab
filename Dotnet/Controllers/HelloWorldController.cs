using Microsoft.AspNetCore.Mvc;
using System.Text.Encodings.Web;

namespace MvcMovie.Controllers;

public class HelloWorldController : Controller
{
    public IActionResult Index()
    {
        return View();
    }

    // --- ZMIENIAMY TĘ AKCJĘ ---
    // GET: /HelloWorld/Welcome/ 
    public IActionResult Welcome(string name, int numTimes = 1)
    {
        // Pakujemy dane do "plecaka" ViewData
        ViewData["Message"] = "Witaj " + name + "!";
        ViewData["NumTimes"] = numTimes;

        return View(); // Odsyłamy do widoku
    }
}