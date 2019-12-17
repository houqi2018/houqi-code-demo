import React from 'react';
import './App.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'

class PastCourse extends React.Component {
    addLikeOrDislike(likeOrDislike) {
        this.props.taken["likeOrDislike"] = likeOrDislike;
        this.props.PastCourseCallback(this.props.taken);
    }

    getLikeOrDislike() {
        if (this.props.taken["likeOrDislike"] === 0) {
            return "N/A";
        }
        else if (this.props.taken["likeOrDislike"] === 1) {
            return "Like";
        }
        else if (this.props.taken["likeOrDislike"] === 2) {
            return "Dislike";
        }
    }

  render() {
    return (
      <Card style={{width: '50%', marginTop: '5px', marginBottom: '5px'}}>
        <Card.Body>
          <Card.Title>{this.props.taken.name}</Card.Title>
          <Card.Subtitle className="mb-2 text-muted">{this.props.taken.number}</Card.Subtitle>
		    <Button variant="primary" onClick={() => this.addLikeOrDislike(1)}>Like</Button>
            <Button variant="primary" onClick={() => this.addLikeOrDislike(2)}>Dislike</Button>
            <p>{this.getLikeOrDislike()}</p>
        </Card.Body>
      </Card>
    )
  }
}

export default PastCourse;
