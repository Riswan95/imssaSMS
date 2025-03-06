function retrieve() {
    $.ajax(
        {
            url: "/retrieveAttendance",
            method: "GET"
        }
    ).done(
        function(data){
            console.log("AJAX CALLED");
            console.log(data);
            presentData(data);
        }
    )
}

function presentData(data){
    console.log('presentData func called.')
    currDate = new Date();
    count = 0;
    $.each(data, function(index,value){
        count++;
        //console.log(index);
        $('#previousSection').append(
            '<h8 class="card-header" id="'+count+'">'+index+'</h8>');
        $.each(data[index],function(index2, value2){
            //console.log(value2)
            bufferDate = new Date(value2);
            if(bufferDate.toDateString() == currDate.toDateString()){
                var list = document.getElementById("classButtons").children;
                $(list).each(function(){
                    if(($(this)[0].innerText) == index)
                        console.log(($(this)[0].innerText) + ' attendance taken.');
                        console.log(($(this)[0]));
                })
            }
            //console.log(bufferDate.toDateString())
            //console.log('#'+count);
            $('#'+count).append(
                "<ul class=" + "list-group list-group-flush"+">"+bufferDate.toDateString()+"</ul>");
        });
        // console.log(bufferDate.toDateString());
        // console.log(currDate.toDateString());
        // 
        //     console.log('Attendance for today is taken');
        //     $('#todaySection').empty();
        //     $('#todaySection').append('ATTENDANCE ALREADY TAKEN FOR TODAY! :D');
        // }
        
    });
}