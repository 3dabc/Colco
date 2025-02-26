'use client';
//client side instead of server side

import {db} from "@/firebase";
import {useEffect, useState} from 'react';
import {doc, collection, setDoc, getDoc, getDocs, addDoc, updateDoc, deleteDoc} from 'firebase/firestore';
import {useRouter} from 'next/navigation';
// import {useRouter} from 'next/router';
import {
  Box,
  Button,
  Container,
  TextField,
  Typography,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Grid,
  Paper,
  Card,
  CardActionArea,
} from "@mui/material";
// import { Email } from "@clerk/backend/dist/api";


export default function Home() {

// failed first attempt of the savedata func
  // const saveData = async() => {
  //   const batch = writeBatch(db);
  //   const userDocRef = doc(collection(db, 'users'), user.id);
  //   const docSnap = await getDoc(userDocRef);
  // }
  
  /*
  THIS WILL CHANGE BCUS I HAVE NO IDEA WHAT DATA WE ARE STORING YET :)))))
  */
  const [users, setUsers] = useState([]);
  const [events, setEvents] = useState([]);
  const [sensors, setSensors] = useState([]);
  const [FName, setFName] = useState('');
  const [LName, setLName] = useState('');
  const [userEmail, setUserEmail] = useState('');
  const [Pword, setPword] = useState('');
  // const [sensorAddy,setSensorAddy] = useState('');
  // const [sensorType,setSensorType] = useState('');
  const [LThresh,setLThresh] = useState('');
  const [HThresh,setHThresh] = useState('');
  const [dataType,setDataType] = useState('');
  const [metric,setMetric] = useState('');
  const [title, setTitle] = useState('');

  const [userIdToUpdate, setUserIdToUpdate] = useState('');
  const [eventIdToUpdate, setEventIdToUpdate] = useState('');

  useEffect(() => {
    fetchUserData();
    fetchEventData();
    // fetchSensorData();
  }, []);

  const fetchUserData = async() => {
    const querySnap = await getDocs(collection(db, 'User'));
    const userData =[];
    querySnap.forEach((foo) => {
      userData.push({id: foo.id, ...foo.data()});
    });
    setUsers(userData);
  };

  const fetchEventData = async() => {
    const querySnap = await getDocs(collection(db, 'Event'));
    const eventData=[];
    querySnap.forEach((foo) => {
      eventData.push({id: foo.id, ...foo.data()});
    });
    setEvents(eventData);
  };

  const fetchSensorData = async() => {
    const querySnap = await getDocs(collection(db, 'Sensor'));
    const sensorData = [];
    querySnap.forEach((foo) => {
      sensorData.push({id: foo.id, ...foo.data()});
    });
    setSensors(sensorData);
  }
  
  const newUser = async() => {
    const newDocRef = doc(collection(db,'User'));
    await setDoc(newDocRef, { 
      FirstName: FName,
      LastName: LName,
      Email: userEmail,
      Password: Pword,
    });
    setFName('');
    setLName('');
    setUserEmail('');
    setPword('');
    fetchUserData();
  };

  const newEvent = async() => {
    const newDocRef = doc(collection(db,'Event'));
    await setDoc(newDocRef, {
      LowerThresh: LThresh,
      Metric: HThresh,
      Type: dataType,
      UpperThresh: metric,
      Title: title,
    });
    setLThresh('');
    setHThresh('');
    setDataType('');
    setMetric('');
    setTitle('');
    fetchEventData();
  };

  const updateUser = async () => {
    if (!userIdToUpdate) return;
    await updateDoc(doc(db, 'User', userIdToUpdate), {
      FirstName: FName,
      LastName: LName,
      Email: userEmail,
      Password: Pword,
    });
    setUserIdToUpdate('');
    setFName('');
    setLName('');
    setUserEmail('');
    setPword('');
    fetchUserData();
  };

  const deletUser = async () => {
    await deleteDoc(doc(db, 'User', id));
    fetchUserData();
  };

  const updateEvent = async () => {
    if (!eventIdToUpdate) return;
    await updateDoc(doc(db, 'Event', eventIdToUpdate), {
      Title: title,
      Metric: metric,
      Type: dataType,
      LowerThresh: LThresh,
      UpperThresh: HThresh,
    });
    setEventIdToUpdate('');
    setTitle('');
    setMetric('');
    setDataType('');
    setLThresh('');
    setHThresh('');
    fetchEventData();
  };

  const deleteEvent = async (id) => {
    await deleteDoc(doc(db, 'Event', id));
    fetchEventData();
  };

  return (
    <Container maxWidth='md'>
      <Box color='#b78d6a'
      sx={{mt: 4,
          mb: 6,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",}}>
            <Typography variant="h2" gutterBottom>ColCo Inc.</Typography>
            <Paper sx={{p:2, mb:4, width:'100%'}}>
              <Typography variant="h5">Create New User</Typography>
              <TextField label='First Name' fullWidth variant="outlined" value={FName} onChange={(e)=>setFName(e.target.value)} sx={{mb:2}}/>
              <TextField label='Last Name' fullWidth variant="outlined" value={LName} onChange={(e)=>setLName(e.target.value)} sx={{mb:2}}/>
              <TextField label='Email' fullWidth variant="outlined" value={userEmail} onChange={(e)=>setUserEmail(e.target.value)} sx={{mb:2}}/>
              <TextField label='Password' fullWidth variant="outlined" value={Pword} onChange={(e)=>setPword(e.target.value)} sx={{mb:2}}/>
              <Button variant="contained" color='primary' onClick={newUser}>Save New User</Button>
            </Paper>
          <Typography variant="h3" sx={{mb:2}}>Users List</Typography>
          <Grid container spacing={2} sx={{mb:4}}>
            {users.map((u) => (
              <Grid item key={u.id}>
                <Box border={1} borderRadius={2} p={2}>
                  <Typography variant="h5">{u.FirstName} {u.LastName}</Typography>
                  <Typography variant="h6">Email: {u.Email}</Typography>
                  <Typography variant="h6">Password: {u.Password}</Typography>
                </Box>
              </Grid>
            ))}
          </Grid>
          <Paper sx={{p:2, mb:4, width:'100%'}}>
              <Typography variant="h5">Create New Event</Typography>
              <TextField label='Title' fullWidth variant="outlined" value={title} onChange={(e)=>setTitle(e.target.value)} sx={{mb:2}}/>
              <TextField label='Metric' fullWidth variant="outlined" value={metric} onChange={(e)=>setMetric(e.target.value)} sx={{mb:2}}/>
              <TextField label='Type' fullWidth variant="outlined" value={dataType} onChange={(e)=>setDataType(e.target.value)} sx={{mb:2}}/>
              <TextField label='Lower Threshold' fullWidth variant="outlined" value={LThresh} onChange={(e)=>setLThresh(e.target.value)} sx={{mb:2}}/>
              <TextField label='Upper Threshold' fullWidth variant="outlined" value={HThresh} onChange={(e)=>setHThresh(e.target.value)} sx={{mb:2}}/>
              <Button variant="contained" color='primary' onClick={newEvent}>Save New Event</Button>
            </Paper>
            <Typography variant="h3" sx={{mb:2}}>Events List</Typography>
          <Grid container spacing={2} sx={{mb:4}}>
            {events.map((u) => (
              <Grid item key={u.id}>
                <Box border={1} borderRadius={2} p={2}>
                <Typography variant="h5">Title: {u.Title}</Typography>
                  <Typography variant="h6">Metric: {u.Metric}</Typography>
                  <Typography variant="h6">Type: {u.Type}</Typography>
                  <Typography variant="h6">Lower Threshold: {u.LowerThresh} Upper Threshold: {u.UpperThresh}</Typography>
                </Box>
              </Grid>
            ))}
          </Grid>
      </Box>
      {/* <Typography variant="h5">Hello World!</Typography> */}
    </Container>

  );
}