class LineColors:
    def __init__(self):                
        pass

    @property
    def LM_W(self):
        """White of the Mana Symbol on lands"""
        return (0.98, 0.98, 0.96)
    
    @property
    def LB_W(self):
        """White of the Background on lands"""
        return (0.97, 0.91, 0.73)

    @property
    def MS_W(self):
        """White of the Mana Symbol from 17Lands"""
        return (0.94, 0.95, 0.75)


    @property
    def LM_U(self):
        """Blue of the Mana Symbol on lands"""
        return (0.05, 0.41, 0.67)
    
    @property
    def LB_U(self):
        """Blue of the Background on lands"""
        return (0.7, 0.81, 0.92)

    @property
    def MS_U(self):
        """Blue of the Mana Symbol from 17Lands"""
        return (0.71, 0.8, 0.89)


    @property
    def LM_B(self):
        """Black of the Mana Symbol on lands"""
        return (0.08, 0.04, 0.0)
    
    @property
    def LB_B(self):
        """Black of the Background on lands"""
        return (0.65, 0.62, 0.62)

    @property
    def MS_B(self):
        """Black of the Mana Symbol from 17Lands"""
        return (0.67, 0.64, 0.6)


    @property
    def LM_R(self):
        """Red of the Mana Symbol on lands"""
        return (0.83, 0.13, 0.16)
    
    @property
    def LB_R(self):
        """Red of the Background on lands"""
        return (0.92, 0.62, 0.51)

    @property
    def MS_R(self):
        """Red of the Mana Symbol from 17Lands"""
        return (0.86, 0.53, 0.39)


    @property
    def LM_G(self):
        """Green of the Mana Symbol on lands"""
        return (0.0, 0.45, 0.24)
    
    @property
    def LB_G(self):
        """Green of the Background on lands"""
        return (0.77, 0.83, 0.79)

    @property
    def MS_G(self):
        """Green of the Mana Symbol from 17Lands"""
        return (0.58, 0.71, 0.51)




    @property
    def W(self):
        """White"""
        return (0.84, 0.73, 0.40, 0.85)
    
    @property
    def U(self):
        """Blue"""
        return (0.28, 0.47, 0.82, 0.85)
    
    @property
    def B(self):
        """Black"""
        return (0.24, 0.24, 0.24, 0.85)
    
    @property
    def R(self):
        """Red"""
        return (0.77, 0.31, 0.32, 0.85)
    
    @property
    def G(self):
        """Green"""
        return (0.33, 0.66, 0.41, 0.85)
    

    @property
    def LW(self):
        """Light White"""
        return (1.00, 0.99, 0.64, 0.85)
    
    @property
    def LU(self):
        """Light Blue"""
        return (0.63, 0.79, 0.96, 0.85)
    
    @property
    def LB(self):
        """Light Black"""
        return (0.47, 0.47, 0.47, 0.85)
    
    @property
    def LR(self):
        """Light Red"""
        return (1.00, 0.62, 0.60, 0.85)
    
    @property
    def LG(self):
        """Light Green"""
        return (0.55, 0.90, 0.63, 0.85)

    @property
    def P(self):
        """White"""
        return (0.80, 0.00, 0.80, 0.85)
    
    @property
    def LP(self):
        """White"""
        return (0.90, 0.50, 0.90, 0.85)
    
    def get_col_array(self, filt=None):
        if filt =='':
            return [self.W, self.LW, self.LR, self.G, self.U, self.LU, self.LG, self.B, self.LB, self.R, self.P, self.LP]
        elif filt =='W':
            return [self.U, self.B, self.R, self.G, self.P, self.LP]
        elif filt =='U':
            return [self.W, self.B, self.R, self.G, self.P, self.LP]
        elif filt =='B':
            return [self.W, self.U, self.R, self.G, self.P, self.LP]
        elif filt =='R':
            return [self.W, self.U, self.B, self.G, self.P, self.LP]
        elif filt =='G':
            return [self.W, self.U, self.B, self.R, self.P, self.LP]
        else:
            return None
