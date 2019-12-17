import React from 'react';
import './App.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'

class Cart extends React.Component {
    constructor(props) {
        super(props);
        this.courseRemover = this.courseRemover.bind(this);
    }

    // Remove all three options in one method
    courseRemover(oneCour, removeAllLec, removeAllSub) {
        let temp = this.props.inCart;
        temp = Object.values(temp).filter((cour) => {
            if (removeAllSub) {
                return !(cour.courName === oneCour.courName && cour.lec === oneCour.lec);
            }
            if (removeAllLec) {
                return cour.courName !== oneCour.courName;
            }
            return cour.courName !== oneCour.courName || cour.lec !== oneCour.lec || cour.id !== oneCour.id;
        })
        this.props.cartCallback(temp);
        console.log(temp)
    }

    render() {
        return (
            <div className="outerCard">
            <Card className="innerCard" border="primary" style = {{width:'39%', position:'fixed',top:'8px',right:'5px'}}>
                    <Card.Title>                    Shopping Cart</Card.Title>
                    {this.props.inCart.length !== 0 ?
                        <div>
                            <h6>Your courses (name + lecture + subsection)</h6>
                            <ul className="list-group smallEntry2">{
                                this.props.inCart.map((oneCour, index) => (
                                    <li className="list-group-item" ref={index} key={index}>
                                        {oneCour.courName}&nbsp;&nbsp;
                                        {oneCour.lec}&nbsp;&nbsp;
                                        {oneCour.hasSub ? oneCour.lec === "All" && oneCour.id === "All" ? 
                                            "All" : oneCour.lec === oneCour.id ? "All" : oneCour.id : "N/A"}
                                        <br /><br />
                                        <Button variant="secondary" style={{marginRight:'15px'}} onClick={() => {this.courseRemover(oneCour, false, false)}}>Delete This Only</Button>
                                        {oneCour.hasSub && oneCour.lec !== "All" && oneCour.lec === oneCour.id ? 
                                            <Button variant="secondary" style={{marginRight:'5px'}} onClick={() => {this.courseRemover(oneCour, false, true)}}>Delete Everything in This Section</Button> 
                                            : 
                                            ""}
                                        {oneCour.id === "All" ? 
                                            <Button variant="secondary" onClick={() => {this.courseRemover(oneCour, true, false)}}>Delete Everything in This Lecture</Button>
                                            :
                                            ""}
                                    </li>
                                ))
                            }</ul> 
                        </div>
                        : 
                        <h6>You have no courses.</h6>}
        </Card>
        </div>
        )
    }
}

export default Cart;
