document.getElementById("operation").addEventListener("change", function() {
    if (this.value === "encrypt") {
        document.getElementById("encrypt-section").style.display = "block";
        document.getElementById("decrypt-section").style.display = "none";
    } else {
        document.getElementById("encrypt-section").style.display = "none";
        document.getElementById("decrypt-section").style.display = "block";
    }
});

function encryptFile() {
    let fileInput = document.getElementById("encrypt-file").files[0];
    if (!fileInput) {
        alert("Please select a file to encrypt!");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput);

    fetch("/encrypt", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("encrypt-result").innerHTML = `
            <p>Encryption Successful!</p>
            <a href="${data.encrypted_url}" download>Download Encrypted File</a><br>
            <a href="${data.key_url}" download>Download Key</a>
        `;
    });
}

function decryptFile() {
    let encryptedFile = document.getElementById("decrypt-file").files[0];
    let keyFile = document.getElementById("key-file").files[0];

    if (!encryptedFile || !keyFile) {
        alert("Please select both encrypted file and key file!");
        return;
    }

    let formData = new FormData();
    formData.append("file", encryptedFile);
    formData.append("key", keyFile);

    fetch("/decrypt", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("decrypt-result").innerHTML = `
            <p>Decryption Successful!</p>
            <a href="${data.decrypted_url}" download>Download Decrypted File</a>
        `;
    });
}
