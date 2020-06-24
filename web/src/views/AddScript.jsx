import React, { Component } from "react";
import { Grid, Row, Col } from "react-bootstrap";

import UploadFile from "components/UploadFile/UploadFile";

class AddScript extends Component {

  render() {
    return (
      <div className="content">
        <Grid fluid>
          <Row>
            <Col md={12}>

              <UploadFile />
            </Col>

            <Col md={12}>   
            </Col>
          </Row>
        </Grid>
      </div>
    );
  }
}

export default AddScript;
