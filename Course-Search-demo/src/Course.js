import React from 'react';
import './App.css';
import CourseTable from './CourseTable';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'

class Course extends React.Component {
	constructor(props){
		super(props)
    this.toggleDetail = this.toggleDetail.bind(this)
    this.state = {
      showTable:false
    }
	}
  render() {
    const {showTable} = this.state;
    return (
      <Card style={{width: '50%', marginTop: '5px', marginBottom: '5px'}}>
        <Card.Body>
          <Card.Title>{this.props.data.name}</Card.Title>
          <Card.Subtitle className="mb-2 text-muted">{this.props.data.number} - {this.getCredits()}</Card.Subtitle>
		    <Button variant="primary" onClick={this.toggleDetail}>Show / Hide Details</Button>
        {showTable === true? <CourseTable courseInfo={this.props.data} inCart={this.props.inCart} courseTableCallback={(newCart) => this.props.courseCallback(newCart)}/>:""}
        </Card.Body>
      </Card>
    )
  }
  toggleDetail (event){
    event.preventDefault()
    const {showTable} = this.state
    this.setState({
      showTable: !showTable
    })
  }
  getCredits() {
    if(this.props.data.credits === 1)
      return '1 credit';
    else
      return this.props.data.credits + ' credits';
  }
}

export default Course;
