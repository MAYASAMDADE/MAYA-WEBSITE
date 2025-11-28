$('#slider1, #slider2, #slider3, #slider4').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5, 
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
   // console.log(id)
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id: id
        },
        success: function(data){
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
        }
    })
})

$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
   // console.log(id)
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id: id
        },
        success: function(data){
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
        }
    })
})


$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id: id
        },
        success: function(data){
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})


document.getElementById("search-input").addEventListener("input", function () {
    const query = this.value.trim();

    if (query.length > 0) {
        fetch(`/api/search?query=${encodeURIComponent(query)}`)
            .then((response) => response.json())
            .then((data) => {
                const searchResults = document.getElementById("search-results");
                searchResults.innerHTML = ""; // Clear previous results

                if (data.products.length > 0) {
                    data.products.forEach((product) => {
                        const item = document.createElement("div");
                        item.className = "dropdown-item";
                        item.innerHTML = `
                            <a href="/product-detail/${product.id}">
                                <img src="${product.image}" alt="${product.name}" width="40" />
                                <span>${product.name}</span>
                                <span>₹${product.price}</span>
                            </a>
                        `;
                        searchResults.appendChild(item);
                    });
                    searchResults.style.display = "block"; // Make the dropdown visible
                } else {
                    searchResults.style.display = "none";
                }
            })
            .catch((error) => console.error("Error fetching search results:", error));
    } else {
        document.getElementById("search-results").style.display = "none"; // Hide dropdown if input is empty
    }
    console.log("Search Results:", data.products);
});
