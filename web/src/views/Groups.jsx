import React, { Component } from "react";
import { Grid, Row, Col, Table } from "react-bootstrap";

import Card from "components/Card/Card.jsx";

class Groups extends Component {
  state = {
    groups : {},
    categories : ["id", "name", "last fault", "active"],
    groupsInfoList : [],
    enabledGroupsInfoList : [],
    disabledGroupsInfoList : [],
    groupsUrl : "http://52.255.160.180:5001/group"
  }

  componentDidMount() {
    fetch(this.state.groupsUrl)
    .then(res => res.json())
    .then((data) => {
      var groups_object = data['result']
      this.setStates(groups_object)
      this.reSetStates()
    })
    .catch(console.log)
  }

  reSetStates = () => {
    fetch(this.state.groupsUrl)
    .then(res => res.json())
    .then((data) => {
      var groups_object = data['result']
      this.setStates(groups_object)
    })

    .catch(console.log)

    setTimeout(this.reSetStates, 5000);
  }
  setStates(groups){
    this.setState({groupsInfoList : this.getGroupsList(groups)})
    console.log(this.state)
    this.setState({enabledGroupsInfoList : this.getGroupsByProperty(groups, true)})
    this.setState({disabledGroupsInfoList : this.getGroupsByProperty(groups, false)})
    
}
  getGroupsList(groups){
    var groupsList = []
    for (var i = 0;  i < groups.length ; i++ ){
        var group = groups[i]
        var groupList = this.getGroupList(group,i)
        groupsList.push(groupList)
    }
    return groupsList
  }

  getGroupList(group,i){
    var groupList = [i, group['name'], "NEEDS FIXING", group['active'].toString() ]
    return groupList
  }

  getGroupsByProperty(groupsList, property ){
    var groupsByProperty = []
    
    for (var i = 0;  i < groupsList.length ; i++ ){
        if (Object.values(groupsList[i]).includes(property)) {
            groupsByProperty.push(groupsList[i])
        }
    }
    groupsByProperty = this.getGroupsList(groupsByProperty)
    return groupsByProperty
  }

  render() {
    return (
      <div className="content">
        <Grid fluid>
          <Row>
            <Col md={12}>
              <Card
                title="All Groups"
                category="All Registered Groups"
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
                      {this.state.groupsInfoList.map((prop, key) => {
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
                title="enabled Groups"
                category="Groups That Can be Used In Faults"
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
                      {this.state.enabledGroupsInfoList.map((prop, key) => {
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
                title="Disabled Groups"
                category="Groups That Cannot be Used In Faults"
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
                      {this.state.disabledGroupsInfoList.map((prop, key) => {
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

export default Groups;
