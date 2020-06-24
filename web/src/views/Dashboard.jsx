import React, { Component } from "react";
import ChartistGraph from "react-chartist";
import { Grid, Row, Col } from "react-bootstrap";

import { Card } from "components/Card/Card.jsx";
import { StatsCard } from "components/StatsCard/StatsCard.jsx";

import {
  legendPie,
  dataSales,
  optionsSales,
  responsiveSales,
  legendSales,
  dataBar,
  optionsBar,
  responsiveBar,
  legendBar
} from "variables/Variables.jsx";

class Dashboard extends Component {
  state = {
    logs : {},
    lastUpdated : '',
    logsUrl : 'http://52.255.160.180:5001/logs',
    pieChartData : {}
  }

  componentDidMount() {
    fetch(this.state.logsUrl)
    .then(res => res.json())
    .then((data) => {
      var logs = data['result']
      this.setStates(logs)
      this.reSetStates()
    })
    .catch(console.log)
  }

  setStates(logs){
    this.setState({numOfLogs : logs.length})
    this.setState({lastUpdated :this.getCurrentTime()})
    this.setState({pieChartData : {
      series : this.getPieChartSeries(logs)
    }})
    this.setState({numOfSucceededFaults : this.divideLogsByExitCode(logs)['selfHealedLogs'].length})
    this.setState({numOfFailedFaults : (logs.length - this.divideLogsByExitCode(logs)['selfHealedLogs'].length)})
    this.setState({ascendingLogs : this.orderAscendingLogs(logs)});
    this.setState({timeGraphData : this.getGraphData(this.state.ascendingLogs)});
  }

  reSetStates = () => {
    fetch(this.state.logsUrl)
    .then(res => res.json())
    .then((data) => {
      var logs_object = data['result']
      this.setStates(logs_object)
    })
    .catch(console.log)

    setTimeout(this.reSetStates, 5000);
  }

  
  getLogsList(servers){
    var serversList = []
    for (var i = 0;  i < servers.length ; i++ ){
        var server = servers[i]
        var serverList = this.getServerList(server,i)
        serversList.push(serverList)
    }
    return serversList
  }

  getLogList(server,i){
    var groups = ""
    for (var j = 0; j < server['groups'].length ; j++ ){
        if (j === server['groups'].length - 1){
            groups += server['groups'][j]
        }else {
            groups = server['groups'][j] + ","
        }
        
    }

    var serverList = [i, server['dns'], "NEEDS FIXING", server['active'].toString() , groups  ]
    return serverList
  }


  divideLogsByExitCode(logsList){
    let devidedLogs = {
    'failedFaults' : [],'failedProbesLogs' : [],'failedRollbackLogs' : [],
    'rollbackedLogs' : [], 'selfHealedLogs' : []
    };
    for (var i = 0;  i < logsList.length ; i++ ){
      let logs = logsList[i]['logs'];
      try  { 
        if(logs["successful"]  === false){
          devidedLogs['failedFaults'].push(logsList[i]);
        }else if (logs['probes']['exit_code'] !== "0") {
          devidedLogs['failedProbesLogs'].push(logsList[i])
          }else if (logs['probe_after_method_logs']['exit_code'] === "0"){
            devidedLogs['selfHealedLogs'].push(logsList[i]);
          }else if (logs['probe_after_rollback_logs']['exit_code'] === "0"){
            devidedLogs['rollbackedLogs'].push(logsList[i]);
          }else if (logs['probe_after_rollback_logs']['exit_code'] !== "0"){
            devidedLogs['failedRollbackLogs'].push(logsList[i]);
          }
      } catch(err) {
        devidedLogs['failedFaults'].push(logsList[i]);
      }
    }
    return devidedLogs
  }


  getPieChartSeries(logsList){
    let devidedLogs = this.divideLogsByExitCode(logsList);
    let pieChartSeries = [];
    Object.values(devidedLogs).forEach(element => {
      pieChartSeries.push(this.getPrecentageOfLogType(logsList,element));
    });  
    return pieChartSeries
  }

  getGraphData(ascendingLogs) {
  console.log(ascendingLogs)

  let dates = ascendingLogs.map(log =>  new Date(log['date'].replace(
      /^(\d{4})(\d\d)(\d\d)(\d\d)(\d\d)(\d\d)$/,
      '$4:$5:$6 $2/$3/$1'
  )));
  console.log(dates)

  console.log(dates[dates.length - 1]);

  let numberOfElements = 8
  let timeGap = (dates[dates.length -1].getTime() - dates[0].getTime()) / numberOfElements;
  let labels = []
 
    for (let i = 1; i < numberOfElements; i ++){
      dates[i] = new  Date(dates[i - 1].getTime() + (timeGap));
      
    };

    
    let devidedLogs = this.divideLogsByExitCode(ascendingLogs);
    let selfHealed, rollbacked, failedHealing = new Array(dates.length)
    selfHealed = this.getLogTypeGraphArray(devidedLogs['selfHealedLogs'],dates);
    rollbacked = this.getLogTypeGraphArray(devidedLogs['rollbackedLogs'],dates);
    failedHealing = this.getLogTypeGraphArray(devidedLogs['failedRollbackLogs'],dates);
    
    labels = dates.map(date => (date.getDate()+"/"+date.getMonth()+ "-" + date.getHours() 
    + ":" + date.getHours()));
    let series = [
      selfHealed,rollbacked,failedHealing
    ];
    let graphData = {
      labels,
      series
    };
    return graphData; 
  }

  getLogTypeGraphArray(logsOfType,dates){
    let logTypeGraphArray = []
    for (let i = 1; i < dates.length; i ++) { 
      logTypeGraphArray.push(0)
      for (let j = 0; j < logsOfType.length; j++){
        let check =  new Date(logsOfType[j]['date'].replace(
          /^(\d{4})(\d\d)(\d\d)(\d\d)(\d\d)(\d\d)$/,
          '$4:$5:$6 $2/$3/$1'
      ));
        let from = dates[i - 1];
        let to = dates[i];
        if (check > from && check < to){
          logTypeGraphArray[i -1] ++;
        }
      }
      if (logTypeGraphArray[i -1] === 0){
        logTypeGraphArray[i -1] = null;
      }
    }
    return logTypeGraphArray
  }

  orderAscendingLogs(logsList){
    logsList.sort(function(a, b){return a['date'] - b['date']});
    return logsList
  }

  getPrecentageOfLogType(logsList,logsOfTypeList){
    let numOflogs = logsList.length;
    let numOflogsOfType = logsOfTypeList.length;
    let precentageOfLogType = Math.round((numOflogsOfType  / numOflogs ) * 100);
    return precentageOfLogType
  }



  getCurrentTime(){
    var d = new Date();
    return d.toLocaleString()
  }

  createLegend(json) {
    var legend = [];
    for (var i = 0; i < json["names"].length; i++) {
      var type = "fa fa-circle text-" + json["types"][i];
      legend.push(<i className={type} key={i} />);
      legend.push(" ");
      legend.push(json["names"][i]);
    }
    return legend;
  }
  render() {
    return (
      <div className="content">
        <Grid fluid>
          <Row>
            <Col lg={3} sm={6}>
              <StatsCard
                bigIcon={<i className="pe-7s-bookmarks text-info" />}
                statsText="total runs"
                statsValue= {this.state.numOfLogs}
                statsIcon={<i className="fa fa-clock-o"/>}
                statsIconText={this.state.lastUpdated}
              />
            </Col>
            <Col lg={3} sm={6}>
              <StatsCard
                bigIcon={<i className="pe-7s-check text-success" />}
                statsText="Succseeded faults"
                statsValue={this.state.numOfSucceededFaults}
                statsIcon={<i className="fa fa-clock-o" />}
                statsIconText={this.state.lastUpdated}
              />
            </Col>
            <Col lg={3} sm={6}>
              <StatsCard
                bigIcon={<i className="pe-7s-attention text-danger" />}
                statsText="Failed faults"
                statsValue={this.state.numOfFailedFaults}
                statsIcon={<i className="fa fa-clock-o" />}
                statsIconText={this.state.lastUpdated}
              />
            </Col>
          </Row>
          <Row>
            <Col md={8}>
              <Card
                statsIcon="fa fa-clock-o  "
                id="chartHours"
                title="Faults Behavior"
                category="24 Hours performance"
                stats="Updated 3 minutes ago"
                content={
                  <div className="ct-chart">
                    <ChartistGraph
                      data={this.state.timeGraphData}
                      type="Line"
                      options={optionsSales}
                      responsiveOptions={responsiveSales}
                    />
                  </div>
                }
                legend={
                  <div className="legend">{this.createLegend(legendSales)}</div>
                }
              />
            </Col>
            <Col md={4}>
              <Card
                statsIcon="fa fa-clock-o"
                title="Group Statistics"
                category="All Servers In Group Performance"
                stats={this.state.lastUpdated}
                content={
                  <div
                    id="chartPreferences"
                    className="ct-chart ct-perfect-fourth"
                  >
                    <ChartistGraph data={this.state.pieChartData} type="Pie" />
                  </div>
                }
                legend={
                  <div className="legend">{this.createLegend(legendPie)}</div>
                }
              />
            </Col>
          </Row>

          <Row>
            <Col md={6}>
              <Card
                id="chartActivity"
                title="Resilient Servers To Failed Servers"
                statsIcon="fa fa-check"
                content={
                  <div className="ct-chart">
                    <ChartistGraph
                      data={dataBar}
                      type="Bar"
                      options={optionsBar}
                      responsiveOptions={responsiveBar}
                    />
                  </div>
                }
                legend={
                  <div className="legend">{this.createLegend(legendBar)}</div>
                }
              />
            </Col>
          </Row>
        </Grid>
      </div>
    );
  }
}

export default Dashboard;
