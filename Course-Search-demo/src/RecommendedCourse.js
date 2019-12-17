import React from 'react';
import './App.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'

class RecommendedCourse extends React.Component {
  render() {
    return (
      <Card style={{width: '50%', marginTop: '5px', marginBottom: '5px'}}>
        <Card.Body>
          <Card.Title>{this.props.recommended.name}</Card.Title>
          <Card.Subtitle className="mb-2 text-muted">{this.props.recommended.number}</Card.Subtitle>
          <Card.Subtitle className="mb-2 text-muted">Rating: {this.props.recommended.rating}</Card.Subtitle>
        </Card.Body>
      </Card>
    )
  }
}

export default RecommendedCourse;
