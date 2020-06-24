import React, { Component } from "react";
import { Grid, Row, Col, Table } from "react-bootstrap";

import Card from "components/Card/Card.jsx";

class Servers extends Component {
  state = {
    servers : {},
    categories : ["id", "dns", "last fault", "active", "groups"],
    serversInfoList : [],
    enabledServersInfoList : [],
    disabledServersInfoList : [],
    serversUrl : 'http://52.255.160.180:5001/servers'
  }

  componentDidMount() {
    fetch(this.state.serversUrl)
    .then(res => res.json())
    .then((data) => {
      var servers_object = data['result']
      this.setStates(servers_object)
      this.reSetStates()
    })
    .catch(console.log)
  }

  setStates(servers){
    this.setState({serversInfoList : this.getServersList(servers)})
    this.setState({enabledServersInfoList : this.getServersByProperty(servers, true)})
    this.setState({disabledServersInfoList : this.getServersByProperty(servers, false)})
}

reSetStates = () => {
  fetch(this.state.serversUrl)
  .then(res => res.json())
  .then((data) => {
    var servers_object = data['result']
    this.setStates(servers_object)
  })

  .catch(console.log)

  setTimeout(this.reSetStates, 5000);
}


  getServersList(servers){
    var serversList = []
    for (var i = 0;  i < servers.length ; i++ ){
        var server = servers[i]
        var serverList = this.getServerList(server,i)
        serversList.push(serverList)
    }
    return serversList
  }

  getServerList(server,i){
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

  getServersByProperty(serversList, property ){
    var serversByProperty = []
    
    for (var i = 0;  i < serversList.length ; i++ ){
        if (Object.values(serversList[i]).includes(property)) {
            serversByProperty.push(serversList[i])
        }
    }
    serversByProperty = this.getServersList(serversByProperty)
    return serversByProperty
  }

  render() {
    return (
      <div className="content">
        <Grid fluid>
          <Row>
            <Col md={12}>
              <Card
                title="All Servers"
                category="All Registered Servers"
                ctTableFullWidth
                ctTableResponsive
                content={
                  <Table striped hover>
                    <thead>
                      <tr>
                        {this.state.categories.map((prop, key) => {
                          return <th key={key}>{prop}</th>;
                        })}
                      </tr>
                    </thead>
                    <tbody>
                      {this.state.serversInfoList.map((prop, key) => {
                        return (
                          <tr key={key}>
                            {prop.map((prop, key) => {
                              return <td key={key}>{prop}</td>;
                            })}
                          </tr>
                        );
                      })}
                    </tbody>
                  </Table>
                }
              />
            </Col>

            <Col md={12}>
              <Card
                plain
                title="enabled Servers"
                category="Servers That Can be Used In Faults"
                ctTableFullWidth
                ctTableResponsive
                content={
                  <Table hover>
                    <thead>
                      <tr>
                        {this.state.categories.map((prop, key) => {
                          return <th key={key}>{prop}</th>;
                        })}
                      </tr>
                    </thead>
                    <tbody>
                      {this.state.enabledServersInfoList.map((prop, key) => {
                        return (
                          <tr key={key}>
                            {prop.map((prop, key) => {
                              return <td key={key}>{prop}</td>;
                            })}
                          </tr>
                        );
                      })}
                    </tbody>
                  </Table>
                }
              />
            </Col>
            <Col md={12}>
              <Card
                plain
                title="Disabled Servers"
                category="Servers That Cannot be Used In Faults"
                ctTableFullWidth
                ctTableResponsive
                content={
                  <Table hover>
                    <thead>
                      <tr>
                        {this.state.categories.map((prop, key) => {
                          return <th key={key}>{prop}</th>;
                        })}
                      </tr>
                    </thead>
                    <tbody>
                      {this.state.disabledServersInfoList.map((prop, key) => {
                        return (
                          <tr key={key}>
                            {prop.map((prop, key) => {
                              return <td key={key}>{prop}</td>;
                            })}
                          </tr>
                        );
                      })}
                    </tbody>
                  </Table>
                }
              />
            </Col>
          </Row>
        </Grid>
      </div>
    );
  }
}

export default Servers;
