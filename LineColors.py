class LineColors:
    def __init__(self):                
        pass
    
    @property
    def W(self):
        """White"""
        return (0.85,0.85,0.2,0.8)
    
    @property
    def U(self):
        """White"""
        return (0,0,1,0.8)
    
    @property
    def B(self):
        """White"""
        return (0,0,0,0.8)
    
    @property
    def R(self):
        """White"""
        return (1,0,0,0.8)
    
    @property
    def G(self):
        """White"""
        return (0,0.7,0,0.8)
    
    @property
    def P(self):
        """White"""
        return (1,0,1,0.8)
    
    @property
    def LW(self):
        """White"""
        return (0.85,0.85,0.3,0.5)
    
    @property
    def LU(self):
        """White"""
        return (0,0,1,0.5)
    
    @property
    def LB(self):
        """White"""
        return (0.2,0.2,0.2,0.5)
    
    @property
    def LR(self):
        """White"""
        return (1,0.2,0.2,0.5)
    
    @property
    def LG(self):
        """White"""
        return (0.2,0.7,0.2,0.5)
    
    @property
    def LP(self):
        """White"""
        return (1,0.2,1,0.5)
    
    def get_col_array(self, filt=None):
        if filt =='':
            return [self.W, self.U, self.B, self.R, self.G, self.LW, self.LU, self.LB, self.LR, self.LG, self.P]
        elif filt =='W':
            return [self.U, self.B, self.R, self.G, self.P]
        elif filt =='U':
            return [self.W, self.B, self.R, self.G, self.P]
        elif filt =='B':
            return [self.W, self.U, self.R, self.G, self.P]
        elif filt =='R':
            return [self.W, self.U, self.B, self.G, self.P]
        elif filt =='G':
            return [self.W, self.U, self.B, self.R, self.P]
        else:
            return None
