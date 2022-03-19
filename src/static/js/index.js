let categoriesActives = []

function filtreProduits() {
    let produits = document.getElementsByClassName("produit-all-info");
    let recherche = document.getElementById("input-recherche-produits").value;
    let total = produits.length;

    for(let i = 0; i < produits.length; i++) {
        let element = produits[i];
        element.parentNode.parentNode.classList.remove("display-none");
    }

    for(let i = 0; i < produits.length; i++) {
        let element = produits[i];
        let children = produits[i].children

        let category = children[0].innerHTML;
        let nom = children[1].innerHTML;
        let price = children[2].innerHTML;

        if(!(nom.toLowerCase().includes(recherche.toLowerCase()))) {
            element.parentNode.parentNode.classList.add("display-none");
            total--;
        } else if (categoriesActives.length != 0) {
            if(categoriesActives.indexOf(category) === -1) {
                element.parentNode.parentNode.classList.add("display-none");
                total--;
            }
        }

        if(total === 0) {
            document.getElementById("aucun-item").classList.remove("display-none");
        } else {
            document.getElementById("aucun-item").classList.add("display-none");
        }
    }

}

function ajouteCategorie(categorie) {
    let cat = categorie.id;
    console.log("appel", cat)

    if(categoriesActives.indexOf(cat) === -1) {
        categoriesActives.push(categorie.id);
        categorie.classList.add("category-active")
    } else {
        categoriesActives.splice(categoriesActives.indexOf(cat), 1);
        categorie.classList.remove("category-active");
    }
    console.log(categoriesActives)

    filtreProduits();
}