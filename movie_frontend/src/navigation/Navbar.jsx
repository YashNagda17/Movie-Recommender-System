import React, { useState, useEffect, useRef } from "react";
import { Space, Button, Layout } from "antd";
import SearchIcon from '@mui/icons-material/Search';
// https://discourse.webflow.com/t/add-form-input-to-url/211909


const Navbar = () => {
  const { Header } = Layout;
  const [background, setBackground] = useState("transparent");
  //const [linkColor, setLinkColor] = useState("black");
  // const searchBar = () => {}
  // const [searchInput, setSearchInput] = useState("");
  const movietit = useRef()
  
  
  useEffect(() => {
    const handleScroll = () => {
        
      setBackground("transparent");
      //setLinkColor("black");
    };

    document.addEventListener("scroll", handleScroll);
    // return () => {
    //   document.removeEventListener("scroll", handleScroll);
    // };
  }, []);

  

   
  const routeChange = () =>{ 

    
    const name = movietit.current.value
    movietit.current.value = null;
    
    if (name==='') return;
    
    window.location.href = "/title/" + name;

  }
  

  return (
    <div>
      
      <Header
        style={{
          backgroundColor: `${background}`,
          position: "fixed",
          zIndex: 1,
          width: "36.1%"
        }}
      >
        <Space size={40}>
          <Button type={"primary"} href="/">Home</Button>
          <Button type={"primary"} href="/forms">Review</Button>

          <form>
            <input size="30" type="text" id="searching" ref ={movietit} placeholder="Search by name or keyword.."/>
            <Button type="submit" onClick={routeChange}><SearchIcon style={{ color: "chartreuse" }}/></Button>
          </form>
          
        </Space>
        
      </Header>
      
    </div>
  );
};

export default Navbar;