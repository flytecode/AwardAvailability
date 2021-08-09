// @flow
import logo from './logo.svg';
import './App.css';
import Button from 'react-bootstrap/Button';
import Row from 'react-bootstrap/Row';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useState, useEffect } from 'react'
import React from "react";

type Hotel = {
  'id': number,
  'name': string,
  'brand': string,
}

type Room = {
  'id': number,
  'name': string,
  'hotel_id': number,
}

type Result = {
  'room': Room,
  'availability': [{'start_date': string, 'end_date': string}]
}

function App(): React$Element<any> {
  // not sure about nulls
  const [brandOptions, setBrandOptions] = useState<Array<string>>([]);
  const [hotelOptions, setHotelOptions] = useState<Array<Hotel>>([]);
  const [brand, setBrand] = useState<string | null>(null);
  const [hotel, setHotel] = useState<number | null>(null);
  const [startDate, setStartDate] = useState<string | null>(null);
  const [endDate, setEndDate] = useState<string | null>(null);
  const [results, setResults] = useState<Array<Result>>([]);


  // need to take more care with initial state
  // need to add error handling to api calls
  useEffect(() => {
    fetch('/brands', { method: "POST" }).then(resp => resp.json().then(data => 
      {
        setBrandOptions(data);
      }
    )
    );
  },[])

  function _onChangeBrand(event) {
    const newBrand = event.target.value;
    setBrand(newBrand);
    fetch('/brands/' + newBrand, {method:"POST"}).then(resp => resp.json().then(data => 
    {
      setHotelOptions(data) 
      }
    ) );
  }

  function _getResults(_) {
    fetch(`/brands/${brand}/${hotel}?startDate=${encodeURIComponent(startDate)}&endDate=${encodeURIComponent(endDate)}`,{method: "POST"}).then(resp => 
      resp.json().then(data => {
        console.log(data)
        setResults(data)
    }))
  }
  const brandOptionsComponents = brandOptions.map(brand => <option key={brand + 'Option'}value={brand}>{brand}</option>)
  const hotelOptionsComponents = hotelOptions.map(hotel => <option value={hotel.id} key={hotel.id + 'Option'}>{hotel.name}</option>)
  const resultsComponents = results.map(r => {
    const availability = r.availability.map(a =><Col>{a.start_date} to {a.end_date} </Col> )
    return <Row key={r.room.id + 'Result'}>
      <Col>
        <Row>{r.room.name}</Row>
        <Row>{availability}</Row>
      </Col>
      
    </Row>
  })
  return (
    <Container className="App">
      <Form>
        <Form.Group>
          <Form.Select aria-label="Hotel Brand" onChange={_onChangeBrand}>
            {brandOptionsComponents}
            <option>DUMMY</option>
          </Form.Select>
        </Form.Group>
        <Form.Group>
          <Form.Select aria-label="Hotel" onChange={e => setHotel(e.target.value)}>
            {hotelOptionsComponents}
          </Form.Select>
        </Form.Group>
        <Form.Group>
          <Form.Label>Start Date</Form.Label>
          <Form.Control type="input" onChange={e => setStartDate(e.target.value)}></Form.Control>
        </Form.Group>
        <Form.Group>
          <Form.Label>End Date</Form.Label>
          <Form.Control type="input" onChange={e => setEndDate(e.target.value)}></Form.Control>
        </Form.Group>
        <Button variant="primary" type="button" onClick={_getResults}>
          Submit
        </Button>
      </Form>
      <Container>
        {resultsComponents}
      </Container>
    </Container>
  );
}

export default App;
