document.addEventListener("DOMContentLoaded", () => {
    const tableData = [
        [8103, 83727895, 769158, 31678925, 3294059, 73914, 3512407, 8089170, 1992939, 2120],
        [4567, 8092573, 45013, 29758, 530345, 618475, 12445683, 30127987, 366305, 297539],
        [139723, 45298716, 3295870, 3980, 253970, 579340, 6138, 432063, 81924982, 6583],
        [9813, 32145678, 84673, 139475, 58145469, 13820, 37428981, 63017980, 45607, 13925647],
        [34602458, 3643, 83921, 4512693, 4698723, 836438, 5801, 89063, 23972165, 3263],
        [42915, 5853, 72631, 34670654, 36135, 4626071, 83959, 4959398, 68130, 6301],
        [987302, 9672, 4286158, 7807347, 675246, 946053, 2002193, 6004745, 35671, 1061],
        [5732186, 45013, 84203, 56239, 671302, 3004, 38672168, 80873, 4108, 371903],
        [6837, 183820, 43612063, 90542145, 784352, 3956, 23781, 198378, 187123, 6004216],
        [3407, 1792635, 4067903, 98103, 5624, 780523, 56792604, 37801, 6356791, 93956467],
        [431025, 4297589, 83961, 56465421, 6138940, 4295901, 6476023, 97654985, 13283, 21243],
        [613947, 43169857, 4302, 3251673, 70765583, 760536, 37821245, 4623, 1308418, 9212494],
        [8077, 3824510, 53906, 4389, 80610972, 3120, 760530, 3940, 8405737, 89203],
        [579103, 970943, 42057, 87652143, 3048, 497538, 1230, 93745125, 19081257, 23456]
    ];

    let timerStarted = false;
    let startTime;
    let clickData = [];

    // Function to create table with individual character buttons
    function createTable() {
        const tableBody = document.getElementById('table-body');
        tableData.forEach((rowData, rowIndex) => {
            const row = document.createElement('tr');
            rowData.forEach((cellData, colIndex) => {
                const cell = document.createElement('td');
                const cellString = cellData.toString();
                
                for (let i = 0; i < cellString.length; i++) {
                    const button = document.createElement('button');
                    button.textContent = cellString[i];
                    button.onclick = () => handleClick(rowIndex, colIndex, i, cellString[i]);
                    cell.appendChild(button);
                }
                row.appendChild(cell);
            });
            tableBody.appendChild(row);
        });
    }

    // Function to handle button click
    function handleClick(row, col, index, char) {
        if (!timerStarted) {
            startTime = Date.now();
            timerStarted = true;
        }
        
        const timestamp = Date.now() - startTime;
        clickData.push([row, col, index, timestamp]);
        console.log("Click data:", clickData);
    }

    // Function to handle "Done" button click
    document.getElementById('done-button').onclick = () => {
        const totalDuration = Date.now() - startTime;
        console.log("Final click data:", clickData);
        console.log("Total time (ms):", totalDuration); //Make this is seconds later, currently in miliseconds
        alert(`Total time: ${totalDuration} ms`);
    };

    // Initialize the table
    createTable();
});
