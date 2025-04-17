const selectedList = divContent
        .split(",")            
        .map(str => str.trim()); 

        console.log(selectedList);
        function prepareFormBeforeSubmit() {
            const divContent = document.getElementById("selected-times-hidden").innerText;
            const selectedList = divContent
                .split(",")
                .map(str => str.trim());
        
            const hiddenInput = document.getElementById("class-time-input");
            hiddenInput.value = JSON.stringify(selectedList);  // ← 배열을 문자열로 변환
        
            console.log("✅ 전송할 값:", hiddenInput.value);  // ["월1","화2",...]
        }