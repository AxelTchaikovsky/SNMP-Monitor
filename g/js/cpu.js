
var cpu_time=[];
var i;
for (i=0;i<60;i++)
  cpu_time[i]=i-50;
var cpu_usage=[];
for (i=0;i<60;i++)
  cpu_usage[i]=0;
var config = {
  type: 'line',
  data: {
    labels: cpu_time,
    datasets: [{
      label: 'CPU usage',
      backgroundColor: 'rgb(255, 99, 132)',
      borderColor: 'rgb(255, 99, 132)',
      data: cpu_usage,
      fill: false,
    }]
  },
  options: {
    responsive: true,
    events:['mousemove', 'mouseout', 'click', 'touchstart', 'touchmove'],
    tooltips: {
      mode: 'index',
      intersect: true,
    },
    hover: {
      mode: 'nearest',
      intersect: true,
    },
    scales: {
      xAxes: [{
        display: false,
        scaleLabel: {
          display: true
        }
      }],
      yAxes: [{
        display: true,
        scaleLabel: {
          display: true
        },
        ticks:{
          max:100,
          min:0
        }
      }]
    }
  }
};


var mem_time=[];
var i;
for (i=0;i<60;i++)
  mem_time[i]=i-50;
var mem_usage=[];
for (i=0;i<60;i++)
  mem_usage[i]=0;

  var configm = {
  type: 'line',
  data: {
    labels: mem_time,
    datasets: [{
      label: 'MEM usage',
      backgroundColor: 'rgb(54, 162, 235)',
      borderColor: 'rgb(54, 162, 235)',
      data: mem_usage,
      fill: false,
    }]
  },
  options: {
    responsive: true,
    events:['mousemove'],
    tooltips: {
      mode: 'index',
      intersect: true,
    },
    hover: {
      mode: 'nearest',
      intersect: true,
    },
    scales: {
      xAxes: [{
        display: false,
        scaleLabel: {
          display: true
        }
      }],
      yAxes: [{
        display: true,
        scaleLabel: {
          display: true
        },
        ticks:{
          max:100,
          min:0
        }
      }]
    }
  }
};

// ////////////////////////
var net_time=[];
var i;
for (i=0;i<60;i++)
  net_time[i]=i-50;
var net_in=[];
var net_out=[];
var net_in_sum=[];
var net_out_sum=[];
for (i=0;i<60;i++)
  net_in[i]=0;
  net_out[i]=0;
  net_in_sum[i]=0;
  net_out_sum[i]=0;

var configin = {
  type: 'line',
  data: {
    labels: net_time,
    datasets: [{
      label: 'Net in',
      backgroundColor: 'rgb(12, 99, 132)',
      borderColor: 'rgb(12, 99, 132)',
      data: net_in,
      fill: false,
    },{
      label: 'Net out',
      backgroundColor: 'rgb(132, 132, 99)',
      borderColor: 'rgb(132, 132, 99)',
      data: net_out,
      fill: false,
    }]
  },
  options: {
    responsive: true,
    events:['mousemove', 'mouseout', 'click', 'touchstart', 'touchmove'],
    tooltips: {
      mode: 'index',
      intersect: true,
    },
    hover: {
      mode: 'nearest',
      intersect: true,
    },
    scales: {
      xAxes: [{
        display: false,
        scaleLabel: {
          display: true
        }
      }],
      yAxes: [{
        display: true,
        scaleLabel: {
          display: true
        },
        ticks:{
          max:10,
          min:0
        }
      }]
    }
  }
};
  


////////////////////////////


window.onload = function() {
  var ctx = document.getElementById('cpuchart');
  c1 = new Chart(ctx, config);
  var ctx2 = document.getElementById('memchart');
  c2 = new Chart(ctx2, configm);
  var ctxx = document.getElementById('netchart');
  c3 = new Chart(ctxx, configin);
  getDisk();  
  setInterval(addData,1000);  

};

async function getDisk(){
  let d=await eel.getDisktotal()();
  //console.log(d[0][0]);
  document.getElementById('total1').innerHTML=d[0];
  document.getElementById('total2').innerHTML=d[1];
  document.getElementById('total3').innerHTML=d[2];
  document.getElementById('total4').innerHTML=d[3];
  document.getElementById('total5').innerHTML=d[4];
  document.getElementById('total6').innerHTML=d[5];
  document.getElementById('total7').innerHTML=d[6];
  let e=await eel.getDiskuse()();
  document.getElementById('use1').innerHTML=e[0];
  document.getElementById('use2').innerHTML=e[1];
  document.getElementById('use3').innerHTML=e[2];
  document.getElementById('use4').innerHTML=e[3];
  document.getElementById('use5').innerHTML=e[4];
  document.getElementById('use6').innerHTML=e[5];
  document.getElementById('use7').innerHTML=e[6];
}

async function addData(){
 let n = await eel.getData()();
  addCPUData(n.CPU);
  addMEMData(n.MEM);
  addnetdata(n.netin,n.netout);
}

async function addCPUData(cpu){
  cpu_usage.shift();
  cpu_usage.push(cpu);
  cpu_time.shift();
  cpu_time.push(cpu_time[cpu_time.length-1]+1);
  document.getElementById('cpunum').innerHTML=cpu;
  if (document.getElementById('cputhre').value<cpu){
    document.getElementById('cpunum').className="red-text";
  }
  else document.getElementById('cpunum').className="blue-grey-text";
  c1.update();
}
  
async function addMEMData(mem){
  
  mem_usage.shift();
  mem_usage.push(mem);
  mem_time.shift();
  mem_time.push(mem_time[mem_time.length-1]+1);
  document.getElementById('memnum').innerHTML=mem;
  if (document.getElementById('memthre').value<mem){
    document.getElementById('memnum').className="red-text";
  }
  else document.getElementById('memnum').className="blue-grey-text";
  c2.update();
}

async function addnetdata(netin,netout){
  net_in.shift();
  net_out.shift();
  net_in_sum.push(netin);
  net_in.push(net_in_sum[net_in_sum.length-1]-net_in_sum[net_in_sum.length-2])
  net_out_sum.push(netout);
  net_out.push(net_out_sum[net_out_sum.length-1]-net_out_sum[net_out_sum.length-2])
  net_time.shift();
  net_time.push(net_time[net_time.length-1]+1);
  document.getElementById('netin').innerHTML=net_in[net_in.length-1].toFixed(2);
  document.getElementById('netout').innerHTML=net_out[net_out.length-1].toFixed(2);
  c3.update();
}