import React from 'react';
import './App.css';
import Card from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';
import SearchAndFilter from './SearchAndFilter';

class Sidebar extends React.Component {
  constructor(props) {
    super(props);
    this.tag = React.createRef();
    this.currTag = [];
    this.tagOptions = [];
    this.searchAndFilter = new SearchAndFilter();
    this.subject = React.createRef();
    this.minimumCredits = React.createRef();
    this.maximumCredits = React.createRef();
    this.search = React.createRef();
  }

  setCourses() {
    let filteredData = this.searchAndFilter.searchAndFilter(this.props.untaken, this.currTag);
    this.props.setCourses(filteredData);
  }

  displayDropdown() {
    // Extract keywords as tags from courses dictionary
    Object.values(this.props.untaken).forEach(cour => {
      this.tagOptions = this.tagOptions.concat(cour.keywords);
    })
    // Remove deuplicates
    this.tagOptions = Array.from(new Set(this.tagOptions));
    return this.tagOptions.map((keyword, index) => {
      return (
        <option key={ index }>{ keyword }</option>
      )})
  }
  
  displayAll () {
    this.props.modeCallback(1);
    this.setCourses();
  }

  displayTaken () {
    this.props.modeCallback(2);
    this.setCourses();
  }

  displayRecommended () {
    this.props.modeCallback(3);
    this.setCourses();
  }

  formSubmitter = event => {
    event.preventDefault();
    this.currTag = this.tag.current.value;
    this.setCourses();
    // this.myFormRef.reset();
    this.displayRecommended();
  }

  handleCreditsKeyDown(e) {
    if(['0','1','2','3','4','5','6','7','8','9','Backspace','ArrowLeft','ArrowRight','ArrowUp','ArrowDown','Tab'].indexOf(e.key) === -1)
      e.preventDefault();
  }

  getSubjectOptions() {
    let subjectOptions = [];

    for(const subject of this.props.subjects) {
      subjectOptions.push(<option key={subject}>{subject}</option>);
    }

    return subjectOptions;
  }

  render() {
    return (
      <>
        <Card style={{width: 'calc(20vw - 5px)', marginLeft: '5px', position: 'fixed'}}>
          <Card.Body>
            <Card.Title>Filter</Card.Title>
            <Form onSubmit={this.formSubmitter} ref={(el) => this.myFormRef = el}>
              <Form.Group controlId="formTags" style={{width: '100%'}}>
                <Form.Label>Select an intersted field</Form.Label>
                <Form.Control type="text" placeholder="" autoComplete="off" ref={this.tag} list="myDropdown"/>
                <datalist id="myDropdown" >{this.displayDropdown()}</datalist>
                <br /><button variant="primary" className="btn btn-primary addTag">Go</button>
              </Form.Group>
            </Form>

            <button variant="primary" className="btn btn-primary toggleMode" onClick={this.displayAll.bind(this)}>Show All</button><br /><br />
            <button variant="primary" className="btn btn-primary toggleMode" onClick={this.displayTaken.bind(this)}>Show Taken</button><br /><br />
            <button variant="primary" className="btn btn-primary toggleMode" onClick={this.displayRecommended.bind(this)}>Show Recommended</button><br /><br />

          </Card.Body>
        </Card>
      </>
    )
  }
}

export default Sidebar;
