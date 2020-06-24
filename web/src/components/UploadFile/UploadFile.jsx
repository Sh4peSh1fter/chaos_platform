import React, { Component } from "react";


class UploadFile extends Component {

  render() {
    return (
        <div class="file-upload-wrapper">
        <input type="file" id="input-file-max-fs" class="file-upload" data-max-file-size="2M" />
        </div>
    );
  }
}

export default UploadFile;