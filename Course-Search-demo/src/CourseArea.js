import React from 'react';
import './App.css';
import Course from './Course';
import PastCourse from './PastCourse';
import RecommendedCourse from './RecommendedCourse';

class CourseArea extends React.Component {
  getCourses() {
    let courses = [];
    
    if (this.props.mode === 1) {  // All courses mode
      for(const course of Object.entries(this.props.data)) {
        courses.push (
          <Course data={course[1]} inCart={this.props.inCart} courseCallback={(newCart) => this.props.courseAreaCallback(newCart)}/>
        )
      }
    }
    else if (this.props.mode === 2) {  // Taken courses mode
      for(const course of Object.entries(this.props.taken)) {
        courses.push (
          <PastCourse taken={course[1]} PastCourseCallback={(taken) => this.props.courseAreaCallbackForPastCourse(taken)}/>
        )
      }
    }
    else if (this.props.mode === 3) {  // Recommended courses mode
      for(const course of Object.entries(this.props.untaken)) {
        courses.push (
          <RecommendedCourse recommended={course[1]}/>
        )
      }
    }
    return courses;
  }

  render() {
    return (
      <div style={{margin: '5px'}}>
        {this.getCourses()}
      </div>
    )
  }
}

export default CourseArea;
