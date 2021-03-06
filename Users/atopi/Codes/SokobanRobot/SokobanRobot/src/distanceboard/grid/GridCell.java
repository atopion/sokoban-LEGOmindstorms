package distanceboard.grid;

import javax.imageio.ImageIO;
import javax.swing.*;
import javax.swing.ImageIcon;
import java.awt.*;
import java.awt.event.ComponentEvent;
import java.awt.event.ComponentListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.util.Base64;

public class GridCell extends JPanel implements MouseListener
{
    private CellClickedListener listener;
    private int x;
    private int y;

    // 0 - normal, 1 - wall, 2 - box, 3 - goal, 4 - path vertical, 5 - path horizontal, 6 - path cross, 7 - player
    private int type = 0;

    private JLabel label;

    private String boxString      = /*"data:image/png;base64,*/"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";
    private String targetString   = /*"data:image/png;base64,*/"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";
    private String path_tdString  = /*"data:image/png;base64,*/"iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAB3SURBVGhD7c9BCYBAAAXRBRsYQzCHzUxgB8EWYhpT6Pcm4llnYR5MgCmSftGmPR2PplSVPj0nrrZUFUdoHKFxhMYRGkdoHKFxhMYRGkdoHKFxhMYRGkdoHKFxhMYRGkdoHKFxhKZLbyNrqkqTxrTcmtOQJH2ulBNIovW0LUFpjwAAAABJRU5ErkJggg==";
    private String path_lrString  = /*"data:image/png;base64,*/"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";
    private String path_crString  = /*"data:image/png;base64,*/"iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAEC0lEQVR4Xu2dMYoVURREaxBjY5dirrgETQZz9yCCSzAxMBDExB24AlMXYS4aCoLS6fjnU1D31/RrjnH9++6cV54x8Hdfaf0/DyV9kPRY0r0L/Di/JL2V9FrS3wvMv9ORV3d6+szhXyQ9nRl1dsoLSR8L51SPOEIB/lzob/7Ni/gk6bp6O4XDjlCAlpY/S3peuJPqERTAx00BfFbVJAYIcGMAHx4G8FlVkxggwI0BfHgYwGdVTWKAADcG8OFhAJ9VNYkBAtwYwIeHAXxW1SQGCHBjAB8eBvBZVZMYIMCNAXx4GMBnVU1igAA3BvDhYQCfVTWJAQLcGMCHhwF8VtUkBghwYwAfHgbwWVWTGCDAjQF8eBjAZ1VNYoAANwbw4WEAn1U1iQEC3BjAh4cBfFbVJAYIcGMAHx4G8FlVkxggwI0BfHgYwGdVTWKAADcG8OFhAJ9VNYkBAtwYwIeHAXxW1SQGCHBjAB8eBvBZVZMYIMCNAXx4GMBnVU1igAA3BvDhYQCfVTWJAQLcGMCHhwF8VtUkBghwYwAfHgbwWVWTGCDAvRng0s/bD9bjowMEzr7vYCtA63n7Az8LIwICJ993sBWg9bz9YHc+OkDg5PsOtgK0focO/AyMCAic/EcsBQiILvZRCrDYhU2vSwGmiS42jwIsdmHT61KAaaKLzaMAi13Y9LoUYJroYvMowGIXNr0uBZgmutg8CrDYhU2vSwGmiS42jwIsdmHT61KAaaKLzaMAi13Y9LoUYJroYvMowGIXNr0uBZgmutg8CrDYhU2vSwGmiS42jwIsdmHT695agJ+SHkyfxrzdEXgn6eXNrbb/FPpG0qvdrctCkwR+S3ok6dupAmwluJb0RNL9yVNLs56Vzvku6WvprMljfkh6f+ryt0P4cqiPmi+H+qyqydYXWyhA9Vr9wyiAz+q/JL8CfHgYwGdVTWKAADcG8OFhAJ9VNYkBAtwYwIeHAXxW1SQGCHBjAB8eBvBZVZMYIMCNAXx4GMBnVU1igAA3BvDhYQCfVTWJAQLcGMCHhwF8VtUkBghwYwAfHgbwWVWTGCDAjQF8eBjAZ1VNYoAANwbw4WEAn1U1iQEC3BjAh4cBfFbVJAYIcGMAHx4G8FlVkxggwI0BfHgYwGdVTWKAADcG8OFhAJ9VNYkBAtwYwIeHAXxW1SQGCHBjAB8eBvBZVZMYIMCNAXx4GMBnVU1igAA3BvDhYQCfVTWJAQLcGMCHhwF8VtUkBghwYwAfHgbwWVWTGCDAjQF8eBjAZ1VNYoAA9xEM0Hrfwcnn7Qfsd/HRIxSg8b6DW5+3v4tbDJY4QgEu/b6Ds8/bD9jv4qNHKMAuQK66BAVY9eaG9qYAQyBXHUMBVr25ob0pwBDIVcf8A7KzAJDPJYpnAAAAAElFTkSuQmCC";
    private String legolas_String = /*"data:image/png;base64,*/"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";

    private BufferedImage box, target, path_td, path_lr, path_cr, legolas;
    private ImageIcon boxIcon, targetIcon, path_td_Icon, path_lr_Icon, path_cr_Icon, legolas_Icon;

    public static interface CellClickedListener
    {
        public void clicked(GridCell cell);
    }

    public GridCell(CellClickedListener listener, int x, int y)
    {
        super();
        this.listener = listener;
        this.addMouseListener(this);
        this.x = x;
        this.y = y;

        this.setLayout(new GridBagLayout());
        label = new JLabel();
        this.add(label);

        //new Thread(() -> {
                byte[] arr1 = Base64.getMimeDecoder().decode(boxString);
                try { box = ImageIO.read(new ByteArrayInputStream(arr1)); } catch (Exception e) { e.printStackTrace(); }
                byte[] arr2 = Base64.getMimeDecoder().decode(targetString);
                try { target = ImageIO.read(new ByteArrayInputStream(arr2)); } catch (Exception e) { e.printStackTrace(); }
                byte[] arr3 = Base64.getMimeDecoder().decode(path_tdString);
                try { path_td = ImageIO.read(new ByteArrayInputStream(arr3)); } catch (Exception e) { e.printStackTrace(); }
                byte[] arr4 = Base64.getMimeDecoder().decode(path_lrString);
                try { path_lr = ImageIO.read(new ByteArrayInputStream(arr4)); } catch (Exception e) { e.printStackTrace(); }
                byte[] arr5 = Base64.getMimeDecoder().decode(path_crString);
                try { path_cr = ImageIO.read(new ByteArrayInputStream(arr5)); } catch (Exception e) { e.printStackTrace(); }
                byte[] arr6 = Base64.getMimeDecoder().decode(legolas_String);
                try { legolas = ImageIO.read(new ByteArrayInputStream(arr6)); } catch (Exception e) { e.printStackTrace(); }
        //}).start();
    }

    @Override
    public Dimension getPreferredSize()
    {
        return new Dimension(50, 50);
    }

    public Point getPosition()
    {
        return new Point(x, y);
    }

    public void setColor(Color color)
    {
        this.setBackground(color);
    }

    public void reset()
    {
        this.type = 0;
        this.setBackground(new Color(210, 210, 210));
        this.label.setText("");
        this.label.setIcon(null);
    }

    public boolean isNormal()
    {
        return this.type == 0;
    }

    public void setWall()
    {
        this.type = 1;
        this.setBackground(Color.darkGray);
    }

    public boolean isWall()
    {
        return this.type == 1;
    }

    public void setBox()
    {
        this.type = 2;
        this.label.setIcon(boxIcon);
    }

    public boolean isBox()
    {
        return this.type == 2;
    }

    public void setTarget()
    {
        this.type = 3;
        this.label.setIcon(targetIcon);
    }

    public boolean isTarget()
    {
        return this.type == 3;
    }

    public void setPath_vert()
    {
        this.resizeIcons();
        if(this.isPath_horiz())
            this.setPath_cross();
        else {
            this.type = 4;
            this.label.setIcon(path_td_Icon);
        }
    }

    public boolean isPath_vert() { return this.type == 4; }

    public void setPath_horiz()
    {
        this.resizeIcons();
        if(this.isPath_vert())
            this.setPath_cross();
        else {
            this.type = 5;
            this.label.setIcon(path_lr_Icon);
        }

    }

    public boolean isPath_horiz() { return this.type == 5; }

    public void setPath_cross()
    {
        this.resizeIcons();
        this.type = 6;
        this.label.setIcon(path_cr_Icon);
    }

    public boolean isPath_cross() { return this.type == 6; }

    public void setPlayer()
    {
        this.resizeIcons();
        this.type = 7;
        this.label.setIcon(legolas_Icon);
    }

    public boolean isPlayer()
    {
        return this.type == 7;
    }

    @Override
    public void mouseExited(MouseEvent e) { }

    @Override
    public void mouseEntered(MouseEvent e) { }

    @Override
    public void mouseReleased(MouseEvent e) { }

    @Override
    public void mousePressed(MouseEvent e) { }

    @Override
    public void mouseClicked(MouseEvent e)
    {
        this.resizeIcons();
        this.listener.clicked(this);
    }

    public void resizeIcons()
    {
        boxIcon      = new ImageIcon(box.getScaledInstance((int) (this.getWidth() * 0.8), (int) (this.getHeight() * 0.8), Image.SCALE_SMOOTH));
        targetIcon   = new ImageIcon(target.getScaledInstance((int) (this.getWidth() * 0.8), (int) (this.getHeight() * 0.8), Image.SCALE_SMOOTH));
        path_cr_Icon = new ImageIcon(path_cr.getScaledInstance((int) (this.getWidth() * 0.8), (int) (this.getHeight() * 0.8), Image.SCALE_SMOOTH));
        path_lr_Icon = new ImageIcon(path_lr.getScaledInstance((int) (this.getWidth() * 0.8), (int) (this.getHeight() * 0.8), Image.SCALE_SMOOTH));
        path_td_Icon = new ImageIcon(path_td.getScaledInstance((int) (this.getWidth() * 0.8), (int) (this.getHeight() * 0.8), Image.SCALE_SMOOTH));
        legolas_Icon = new ImageIcon(legolas.getScaledInstance((int) (this.getWidth() * 0.8), (int) (this.getHeight() * 0.8), Image.SCALE_SMOOTH));
    }
}
