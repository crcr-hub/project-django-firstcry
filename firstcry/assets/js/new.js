var myDiv = document.getElementById("myDiv");

myDiv.addEventListener("mouseenter", function() {
  // Add shadow when the mouse enters the element
  myDiv.style.boxShadow = "5px 5px 10px rgba(0, 0, 0, 0.5)";
});

myDiv.addEventListener("mouseleave", function() {
  // Remove shadow when the mouse leaves the element
  myDiv.style.boxShadow = "none";
});